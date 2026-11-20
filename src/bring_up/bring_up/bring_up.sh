#!/bin/bash
source /opt/ros/humble/setup.bash
# Workspace this script lives in (src/bring_up/bring_up/), so each worktree runs its own build.
cd "$(dirname "$(readlink -f "$0")")/../../.."
source install/setup.bash

trap 'kill 0' EXIT   # stop all nodes (incl. ros2 run's children) on exit/Ctrl+C

# Same chain as bringup.launch.py's follow mode: joystick /cmd_vel_joy ->
# twist_mux -> /cmd_vel_mux -> ultrasonic_estop (blocks forward motion near
# obstacles) -> /cmd_vel_safe -> motors.
ros2 run joy joy_node &            # background it so script continues
# e_stop defaults are PS4 via hid-generic: Cross = 1 stops, Options = 9 arms
ros2 run bring_up e_stop &
ros2 run bring_up ps4_teleop --ros-args -p cmd_vel_topic:=cmd_vel_joy &
ros2 launch ultrasonic_pkg ultrasonic_publisher.launch.py &
ros2 run bring_up ultrasonic_estop --ros-args \
    -r cmd_vel_in:=cmd_vel_mux -r cmd_vel_out:=cmd_vel_safe &
ros2 run twist_mux twist_mux --ros-args \
    --params-file "$(ros2 pkg prefix bring_up)/share/bring_up/config/twist_mux.yaml" \
    -r cmd_vel_out:=cmd_vel_mux &
ros2 run bring_up diff_drive_controller --ros-args -p cmd_vel_topic:=cmd_vel_safe
