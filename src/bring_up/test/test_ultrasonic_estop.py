import math

from bring_up.ultrasonic_estop import UltrasonicLogic


def make(required=2):
    return UltrasonicLogic(['left', 'center', 'right'], min_safe_distance=0.15,
                           max_reading_age=1.0, required_readings=required)


def test_clear_with_no_readings():
    assert not make().unsafe(now=0.0)


def test_single_close_reading_is_ignored():
    logic = make()
    logic.on_range('center', 0.29, now=0.00)
    logic.on_range('center', 0.05, now=0.05)  # one-off glitch
    assert not logic.unsafe(now=0.06)
    logic.on_range('center', 0.29, now=0.10)
    assert not logic.unsafe(now=0.11)


def test_two_close_readings_in_a_row_stop():
    logic = make()
    logic.on_range('center', 0.10, now=0.00)
    logic.on_range('center', 0.11, now=0.05)
    assert logic.unsafe(now=0.06)


def test_close_readings_must_be_consecutive():
    logic = make()
    logic.on_range('right', 0.10, now=0.00)
    logic.on_range('right', 0.40, now=0.05)
    logic.on_range('right', 0.10, now=0.10)
    assert not logic.unsafe(now=0.11)


def test_counts_are_per_sensor():
    logic = make()
    logic.on_range('left', 0.10, now=0.00)
    logic.on_range('right', 0.10, now=0.05)
    assert not logic.unsafe(now=0.06)


def test_clears_after_one_far_reading():
    logic = make()
    logic.on_range('left', 0.10, now=0.00)
    logic.on_range('left', 0.10, now=0.05)
    assert logic.unsafe(now=0.06)
    logic.on_range('left', 0.60, now=0.10)
    assert not logic.unsafe(now=0.11)


def test_no_echo_is_clear():
    logic = make()
    logic.on_range('center', math.inf, now=0.00)
    logic.on_range('center', math.inf, now=0.05)
    assert not logic.unsafe(now=0.06)


def test_stale_readings_are_ignored():
    logic = make()
    logic.on_range('center', 0.10, now=0.00)
    logic.on_range('center', 0.10, now=0.05)
    assert not logic.unsafe(now=1.10)


def test_required_readings_of_one_stops_immediately():
    logic = make(required=1)
    logic.on_range('center', 0.10, now=0.00)
    assert logic.unsafe(now=0.01)


def test_stale_lists_silent_sensors():
    logic = make()
    assert logic.stale(now=0.0) == ['left', 'center', 'right']  # never heard from
    logic.on_range('left', 1.0, now=0.0)
    logic.on_range('center', 1.0, now=0.0)
    logic.on_range('right', 1.0, now=0.5)
    assert logic.stale(now=1.2) == ['left', 'center']


def blocked():
    logic = make()
    logic.on_range('center', 0.10, now=0.00)
    logic.on_range('center', 0.10, now=0.05)
    return logic


def test_blocked_stops_forward_only():
    logic = blocked()
    assert logic.limit_forward(0.5, now=0.06) == 0.0
    assert logic.limit_forward(-0.5, now=0.06) == -0.5  # reverse away
    assert logic.limit_forward(0.0, now=0.06) == 0.0    # turn in place


def test_clear_passes_forward():
    assert make().limit_forward(0.5, now=0.0) == 0.5


def make_fail_closed():
    return UltrasonicLogic(['left', 'center', 'right'], min_safe_distance=0.15,
                           max_reading_age=1.0, required_readings=2, fail_closed=True)


def fresh_and_clear(logic, now):
    for frame_id in ('left', 'center', 'right'):
        logic.on_range(frame_id, 1.0, now=now)


def test_fail_closed_blocks_forward_with_no_readings_ever():
    logic = make_fail_closed()
    assert logic.unsafe(now=0.0)
    assert logic.limit_forward(0.5, now=0.0) == 0.0


def test_fail_closed_still_allows_reverse_and_turning():
    logic = make_fail_closed()
    assert logic.limit_forward(-0.3, now=0.0) == -0.3
    assert logic.limit_forward(0.0, now=0.0) == 0.0


def test_fail_closed_one_silent_sensor_blocks_forward():
    logic = make_fail_closed()
    fresh_and_clear(logic, now=0.0)
    assert not logic.unsafe(now=0.5)
    logic.on_range('left', 1.0, now=1.2)
    logic.on_range('center', 1.0, now=1.2)  # right has gone quiet
    assert logic.unsafe(now=1.3)
    assert logic.limit_forward(0.5, now=1.3) == 0.0


def test_fail_closed_recovers_when_the_sensor_returns():
    logic = make_fail_closed()
    assert logic.unsafe(now=0.0)
    fresh_and_clear(logic, now=0.1)
    assert not logic.unsafe(now=0.2)
    assert logic.limit_forward(0.5, now=0.2) == 0.5


def test_default_is_still_fail_open():
    assert not make().fail_closed
    assert not make().unsafe(now=5.0)
