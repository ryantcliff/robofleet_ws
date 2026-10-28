"""diff_drive_controller against fake ODrives: idle on connect, survive a lost ODrive."""
import importlib
import sys
import types

import pytest
import rclpy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

IDLE, CLOSED_LOOP = 1, 8


class DeviceLostException(Exception):
    pass


class TransportException(Exception):
    pass


class FakeDevice:
    """Records axis writes; raises DeviceLostException once unplugged."""

    def __init__(self):
        self.lost = False
        self.state = CLOSED_LOOP  # as left by startup_closed_loop_control
        self.input_vel = 0.0
        dev = self

        class Controller:
            config = types.SimpleNamespace()

            @property
            def input_vel(self):
                return dev.input_vel

            @input_vel.setter
            def input_vel(self, value):
                dev._check()
                dev.input_vel = value

        class Encoder:
            @property
            def vel_estimate(self):
                dev._check()
                return dev.input_vel

        class Axis:
            controller = Controller()
            encoder = Encoder()

            @property
            def requested_state(self):
                return dev.state

            @requested_state.setter
            def requested_state(self, value):
                dev._check()
                dev.state = value

        self.axis0 = Axis()

    def _check(self):
        if self.lost:
            raise DeviceLostException('disconnected')

    def clear_errors(self):
        self._check()


class FakeBus:
    def __init__(self):
        self.devices = {}
        self.unplugged = set()

    def find_sync(self, serial_number=None, timeout=None):
        if serial_number in self.unplugged:
            raise TimeoutError(serial_number)
        self.devices[serial_number] = FakeDevice()
        return self.devices[serial_number]


@pytest.fixture
def bus(monkeypatch):
    bus = FakeBus()
    odrive = types.ModuleType('odrive')
    odrive.find_sync = bus.find_sync
    enums = types.ModuleType('odrive.enums')
    enums.AxisState = types.SimpleNamespace(IDLE=IDLE, CLOSED_LOOP_CONTROL=CLOSED_LOOP)
    enums.InputMode = types.SimpleNamespace(VEL_RAMP=2)
    enums.ControlMode = types.SimpleNamespace(VELOCITY_CONTROL=2)
    libodrive = types.ModuleType('odrive.libodrive')
    libodrive.DeviceLostException = DeviceLostException
    libodrive.TransportException = TransportException
    monkeypatch.setitem(sys.modules, 'odrive', odrive)
    monkeypatch.setitem(sys.modules, 'odrive.enums', enums)
    monkeypatch.setitem(sys.modules, 'odrive.libodrive', libodrive)
    return bus


@pytest.fixture
def node(bus):
    rclpy.init()
    try:
        module = importlib.import_module('bring_up.diff_drive_controller')
        module = importlib.reload(module)  # pick up the fake odrive
        node = module.DiffDriveController()
        node.serials = module.SERIAL_NUMBERS
        yield node
        node.destroy_node()
    finally:
        rclpy.try_shutdown()


def dev(node, bus, name):
    return bus.devices[node.serials[name]]


def states(node, bus):
    return {name: dev(node, bus, name).state for name in node.serials}


def forward(node):
    msg = Twist()
    msg.linear.x = 0.5
    node._cmd_vel_cb(msg)


def test_connect_idles_every_axis(node, bus):
    assert set(states(node, bus).values()) == {IDLE}


def test_release_arms_every_axis(node, bus):
    node._e_stop_cb(Bool(data=False))
    assert set(states(node, bus).values()) == {CLOSED_LOOP}


def test_lost_odrive_while_arming_idles_the_others(node, bus):
    dev(node, bus, 'RR').lost = True
    node._e_stop_cb(Bool(data=False))  # used to raise DeviceLostException
    assert node.stopped
    assert all(state == IDLE for name, state in states(node, bus).items() if name != 'RR')


def test_lost_odrive_while_driving_idles_the_others(node, bus):
    node._e_stop_cb(Bool(data=False))
    dev(node, bus, 'FL').lost = True
    forward(node)
    assert node.stopped
    assert all(state == IDLE for name, state in states(node, bus).items() if name != 'FL')


def test_stays_stopped_while_an_odrive_is_missing(node, bus):
    bus.unplugged.add(node.serials['RR'])
    dev(node, bus, 'RR').lost = True
    node._e_stop_cb(Bool(data=False))
    node._reconnect()
    node._e_stop_cb(Bool(data=True))
    node._e_stop_cb(Bool(data=False))
    assert node.stopped
    assert states(node, bus)['FR'] == IDLE


def test_reconnect_needs_cross_then_options(node, bus):
    bus.unplugged.add(node.serials['RR'])
    dev(node, bus, 'RR').lost = True
    node._e_stop_cb(Bool(data=False))
    bus.unplugged.clear()
    node._reconnect()
    assert states(node, bus)['RR'] == IDLE  # the replacement handle is idled too

    node._e_stop_cb(Bool(data=False))  # e_stop still reports released: stay idle
    assert node.stopped
    node._e_stop_cb(Bool(data=True))   # Cross
    node._e_stop_cb(Bool(data=False))  # Options
    assert not node.stopped
    assert set(states(node, bus).values()) == {CLOSED_LOOP}


def test_shutdown_with_a_lost_odrive_does_not_raise(node, bus):
    node._e_stop_cb(Bool(data=False))
    dev(node, bus, 'RL').lost = True
    node._stop_motors()
    assert states(node, bus)['FR'] == IDLE
