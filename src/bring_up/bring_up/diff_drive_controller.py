import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from bring_up.e_stop import E_STOP_QOS
import odrive
from odrive.enums import AxisState, InputMode, ControlMode
from odrive.libodrive import DeviceLostException, TransportException
import math


WHEEL_RADIUS = 0.125       # meters (25 cm wheels, measured 2026-09-26)
WHEEL_SEPARATION = 0.74    # meters, left to right wheel centers (measured 2026-09-26)
GEAR_RATIO = 30.0        # 30:1 gearbox

SERIAL_NUMBERS = {
    "FR": "316633543334",
    "FL": "357B358B3135",
    "RR": "336636543334",
    "RL": "336536573334",
}

E_STOP_TIMEOUT = 0.5     # seconds without /e_stop before stopping
CMD_VEL_TIMEOUT = 0.5    # seconds without /cmd_vel before commanding zero
RECONNECT_PERIOD = 1.0   # seconds between attempts to find a lost ODrive
RECONNECT_TIMEOUT = 0.5  # seconds each attempt may block the executor

# Raised when an ODrive drops off USB (seen when the motors energize).
ODRIVE_LOST = (DeviceLostException, TransportException)

FAST_DECEL = 50.0
STD_ACCEL  = 10.0


class DiffDriveController(Node):
    def __init__(self):
        super().__init__('diff_drive_controller')
        self.drives = {}
        self.stopped = True
        self._last_e_stop = None
        self._last_cmd_vel = None
        self._moving = False
        self._lost = set()
        # Set when an ODrive drops; cleared by the operator pressing Cross (e-stop
        # engaged) once every ODrive is back. Options then re-arms as usual.
        self._fault = False
        self._connect()
        self.create_subscription(Bool, 'e_stop', self._e_stop_cb, E_STOP_QOS)
        self.create_timer(0.1, self._watchdog)
        self.create_timer(RECONNECT_PERIOD, self._reconnect)
        # bringup.launch.py sets this to twist_mux's output; bring_up.sh keeps cmd_vel.
        cmd_vel_topic = self.declare_parameter('cmd_vel_topic', 'cmd_vel').value
        self.create_subscription(Twist, cmd_vel_topic, self._cmd_vel_cb, 10)
        self.get_logger().info(
            'Diff drive controller ready, idle until /e_stop is released')

    def _connect(self):
        for name, serial in SERIAL_NUMBERS.items():
            self.get_logger().info(f'Connecting to {name} ({serial})...')
            self.drives[name] = self._open(serial)
            self.get_logger().info(f'{name} connected')

    def _open(self, serial, timeout=None):
        dev = odrive.find_sync(serial_number=serial, timeout=timeout)
        dev.clear_errors()
        dev.axis0.controller.config.input_mode = InputMode.VEL_RAMP
        dev.axis0.controller.config.vel_ramp_rate = STD_ACCEL
        dev.axis0.controller.config.vel_gain = 0.02          # default ~0.16, lower = less resistance
        dev.axis0.controller.config.vel_integrator_gain = 0.05
        # Axes stay idle until the e-stop is released, whatever state the
        # ODrive booted or was left in.
        self._idle(dev)
        return dev

    def _reconnect(self):
        for name in sorted(self._lost):
            try:
                self.drives[name] = self._open(SERIAL_NUMBERS[name], RECONNECT_TIMEOUT)
            except (TimeoutError, *ODRIVE_LOST):  # not back yet, or dropped again mid-setup
                continue
            self._lost.discard(name)
            done = '' if self._lost else ': press Cross, then Options, to re-arm'
            self.get_logger().warn(f'{name} reconnected{done}')

    def _drive(self, name, action):
        # Runs action(dev) on one ODrive; a lost ODrive stops the whole robot.
        if name in self._lost:
            return False
        try:
            action(self.drives[name])
            return True
        except ODRIVE_LOST:
            self._lost.add(name)
            self._fault = True
            self.get_logger().error(f'{name} ODrive lost: idling the others')
            self._stop_motors()
            self.stopped = True
            return False

    def _now(self):
        return self.get_clock().now().nanoseconds * 1e-9

    @staticmethod
    def _idle(dev):
        dev.axis0.controller.input_vel = 0.0
        dev.axis0.requested_state = AxisState.IDLE

    @staticmethod
    def _arm(dev):
        dev.clear_errors()
        dev.axis0.controller.input_vel = 0.0
        dev.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL

    def _stop_motors(self):
        self._moving = False
        for name in self.drives:
            self._drive(name, self._idle)

    def _set_velocity(self, name: str, target_vel: float):
        return self._drive(name, lambda dev: self._write_velocity(dev, target_vel))

    @staticmethod
    def _write_velocity(dev, target_vel: float):
        current_vel = dev.axis0.encoder.vel_estimate

        slowing_down = abs(target_vel) < abs(current_vel)
        changing_dir = target_vel * current_vel < 0

        if slowing_down or changing_dir:
            dev.axis0.controller.config.vel_ramp_rate = FAST_DECEL
        else:
            dev.axis0.controller.config.vel_ramp_rate = STD_ACCEL

        dev.axis0.controller.input_vel = target_vel

    def _set_stopped(self, stopped):
        if stopped == self.stopped:
            return
        if not stopped and self._fault:
            self.get_logger().warn(
                'Not arming after a lost ODrive: '
                + (f'waiting for {", ".join(sorted(self._lost))}' if self._lost
                   else 'press Cross, then Options'),
                throttle_duration_sec=2.0)
            return
        self.stopped = stopped
        if stopped:
            self._stop_motors()
            self.get_logger().warn('E-stop: motors idled')
        else:
            for name in self.drives:
                if not self._drive(name, self._arm):
                    return
            self.get_logger().info('E-stop released: motors enabled')

    def _e_stop_cb(self, msg: Bool):
        self._last_e_stop = self._now()
        if msg.data and self._fault and not self._lost:
            self._fault = False
            self.get_logger().info('Lost-ODrive fault cleared: press Options to arm')
        self._set_stopped(msg.data)

    def _watchdog(self):
        if self._last_e_stop is None or self._now() - self._last_e_stop > E_STOP_TIMEOUT:
            self._set_stopped(True)
        elif self._moving and self._now() - self._last_cmd_vel > CMD_VEL_TIMEOUT:
            # Stale command: hold zero velocity but stay armed.
            self.get_logger().warn('No /cmd_vel for 0.5 s: commanding zero')
            for name in self.drives:
                if not self._set_velocity(name, 0.0):
                    break
            self._moving = False

    def _cmd_vel_cb(self, msg: Twist):
        if self.stopped:
            return
        self._last_cmd_vel = self._now()
        v = msg.linear.x
        w = msg.angular.z
        self._moving = v != 0.0 or w != 0.0
        print(f"cmd_vel → linear: {v}, angular: {w}")

        v_left  = v - (w * WHEEL_SEPARATION / 2.0)
        v_right = v + (w * WHEEL_SEPARATION / 2.0)
        print(f"v_left: {v_left} m/s, v_right: {v_right} m/s")

        turns_left  = (v_left  / (2.0 * math.pi * WHEEL_RADIUS)) * GEAR_RATIO
        turns_right = (v_right / (2.0 * math.pi * WHEEL_RADIUS)) * GEAR_RATIO

        # Left wheels are negated to match physical mounting orientation
        (self._set_velocity("FL",  turns_left)
         and self._set_velocity("RL",  turns_left)
         and self._set_velocity("FR", -turns_right)
         and self._set_velocity("RR", -turns_right))

    def destroy_node(self):
        self.get_logger().info('Shutting down — stopping and idling motors')
        self._stop_motors()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = DiffDriveController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
