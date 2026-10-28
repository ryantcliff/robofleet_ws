#!/usr/bin/env python3
import copy
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

CMD_TIMEOUT = 0.5  # seconds; matches diff_drive_controller's /cmd_vel watchdog


class UltrasonicLogic:
    """Decide when the ultrasonic sensors call for a stop.

    A sensor counts as blocked after required_readings consecutive readings
    closer than min_safe_distance, so a single glitched echo doesn't stop the
    robot. One reading at or beyond the limit (including +inf, no echo) clears
    it. Sensors with no reading in max_reading_age are ignored.
    """

    def __init__(self, frame_ids, min_safe_distance, max_reading_age, required_readings):
        self.min_safe_distance = min_safe_distance
        self.max_reading_age = max_reading_age
        self.required_readings = required_readings
        self._close_count = {frame_id: 0 for frame_id in frame_ids}
        self._last_reading = {}

    def on_range(self, frame_id, distance, now):
        if distance < self.min_safe_distance:
            self._close_count[frame_id] = self._close_count.get(frame_id, 0) + 1
        else:
            self._close_count[frame_id] = 0
        self._last_reading[frame_id] = now

    def stale(self, now):
        """Sensors with no reading in max_reading_age; they can't stop the robot."""
        return [frame_id for frame_id in self._close_count
                if frame_id not in self._last_reading
                or now - self._last_reading[frame_id] > self.max_reading_age]

    def unsafe(self, now):
        stale = self.stale(now)
        for frame_id, count in self._close_count.items():
            if frame_id in stale:
                continue  # no recent reading from this sensor
            if count >= self.required_readings:
                return True
        return False

    def limit_forward(self, linear_x, now):
        """Block forward motion while unsafe; reversing and turning stay allowed."""
        return min(linear_x, 0.0) if self.unsafe(now) else linear_x


class UltrasonicEstop(Node):
    """Independent safety failsafe.

    LIDAR-based Nav2 costmap obstacle avoidance is the primary obstacle
    detection system. This node is a last-resort backstop for the LIDAR's
    blind spots (e.g. low obstacles below the scan plane). It sits between
    twist_mux and the motors (cmd_vel_in -> cmd_vel_out) and zeroes forward
    motion while any front ultrasonic sensor reads closer than
    min_safe_distance, so the operator can still reverse or turn away. If this
    node dies the motors get no commands and diff_drive_controller stops them.
    """

    def __init__(self):
        super().__init__('ultrasonic_estop')

        self.declare_parameter('frame_ids', [
            'left_ultrasonic', 'center_ultrasonic', 'right_ultrasonic'])
        # 0.15 m let the robot hit someone at 0.5 m/s (2026-09-30): detection
        # takes up to ~0.2 s and braking ~0.1 m or more.
        self.declare_parameter('min_safe_distance', 0.5)   # meters
        self.declare_parameter('max_reading_age', 1.0)     # seconds
        self.declare_parameter('publish_rate', 20.0)       # Hz, matches the sensors
        # Consecutive close readings before stopping (20 Hz sensors: 2 = ~50 ms)
        self.declare_parameter('required_readings', 2)

        self.frame_ids = self.get_parameter('frame_ids').value
        self.min_safe_distance = self.get_parameter('min_safe_distance').value
        publish_rate = self.get_parameter('publish_rate').value
        self._logic = UltrasonicLogic(
            self.frame_ids, self.min_safe_distance,
            self.get_parameter('max_reading_age').value,
            self.get_parameter('required_readings').value)

        for frame_id in self.frame_ids:
            topic = f'range/{frame_id}'
            self.create_subscription(
                Range, topic,
                lambda msg, fid=frame_id: self._range_callback(msg, fid),
                10)

        self._last_cmd = None       # last command in, unmodified
        self._last_cmd_time = None
        self._last_out_x = 0.0      # linear.x last sent to the motors
        self._out_pub = self.create_publisher(Twist, 'cmd_vel_out', 10)
        self.create_subscription(Twist, 'cmd_vel_in', self._cmd_callback, 10)
        self._timer = self.create_timer(1.0 / publish_rate, self._check_and_publish)

        self.get_logger().info(
            f'Ultrasonic e-stop watching {self.frame_ids} '
            f'at {self.min_safe_distance:.2f} m, '
            f'{self._logic.required_readings} readings in a row')

    def _range_callback(self, msg: Range, frame_id: str):
        self._logic.on_range(frame_id, msg.range, time.monotonic())

    def _cmd_callback(self, msg: Twist):
        self._last_cmd, self._last_cmd_time = msg, time.monotonic()
        self._forward(msg, self._last_cmd_time)

    def _forward(self, msg: Twist, now):
        out = copy.deepcopy(msg)
        out.linear.x = self._logic.limit_forward(msg.linear.x, now)
        self._last_out_x = out.linear.x
        self._out_pub.publish(out)

    def _check_and_publish(self):
        now = time.monotonic()
        stale = self._logic.stale(now)
        if stale:
            # These sensors can't stop the robot; say so rather than fail silently.
            self.get_logger().warn(
                f'No recent reading from {", ".join(stale)}: not guarding those',
                throttle_duration_sec=5.0)
        # An obstacle can appear between commands (Nav2 sends only 10 Hz):
        # block a recent forward command now rather than on the next one.
        if (self._last_out_x > 0.0 and now - self._last_cmd_time < CMD_TIMEOUT
                and self._logic.unsafe(now)):
            self._forward(self._last_cmd, now)


def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicEstop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
