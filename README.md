# RoboFleet — Autonomous Mobile Robot (ROS 2)

This is our ROS 2 workspace for **RoboFleet**, an autonomous rover. This year we have to deliver one FleetBot that follows a GPS RoboBeacon using ROS 2 navigation and localization. The repo has the source code. The write-up, setup and architecture are on the documentation site below.

**[Read the full documentation »](https://robofleet.readthedocs.io/en/latest/)**

> **Name note:** RoboFleet is our 2026-2027 continuation of RoboFlock. Many inherited ROS, config and device names still say `roboflock`. We left them so we do not break things that work.

<!-- Add a short demo clip or photo of the robot here:
![RoboFleet](docs/roboflock.jpg) -->

Here is the robot running SLAM:
https://github.com/user-attachments/assets/d75cb297-7618-43ef-b84b-9466528e4aed

## What it does
- Autonomous navigation with **Nav2**, **SLAM** and `robot_localization`, using **LiDAR + GPS**.
- Custom **ROS 2 nodes** for 2D LiDAR visualization and a differential-drive controller that talks to the **ODrive**-type motor controllers.
- Ultrasonic sensors on an Arduino as an independent obstacle backup. If a sensor goes quiet, forward motion is blocked.
- **RoboBeacon following**: it follows a person carrying the GPS RoboBeacon and stays 1.5-3.0 m away (our follow target is 3 m).
- **Return home / Meshtastic** is still in the code from the last team, but we do not need it this year unless the requirements change.
- Runs on an **NVIDIA Jetson Orin Nano** with custom power and motor wiring.
- Weather protection is a requirement: supervised light rain, splashes and wind-blown alkaline dust. We are not claiming an IP rating for the whole robot.

## Stack
ROS 2 Humble · C++ / Python · Nav2 · SLAM · robot_localization · ODrive · LiDAR · GPS (u-blox) · HC-12 · Meshtastic · NVIDIA Jetson Orin Nano

## Repository layout
```
src/    ROS 2 packages (nodes, controllers, launch, config)
```

## Build
Standard ROS 2 colcon workspace:
```bash
cd robofleet_ws
colcon build
source install/setup.bash
```
The [documentation](https://robofleet.readthedocs.io/en/latest/) covers dependencies, hardware setup and launch instructions.

## Debugging navigation without any hardware (ROS 2 Humble)

Install the navigation packages once:
```bash
sudo apt-get install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-slam-toolbox ros-humble-robot-localization
```

Build and start only the navigation processes, with the lifecycle nodes left unconfigured:
```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select bring_up
source install/setup.bash
ros2 launch bring_up bringup.launch.py hardware:=false enable_mapping:=false autostart:=false
```

This mode does not start sensor drivers, GPS, localization, beacon commands, the
robot state publisher or the motors. It also does not fake any sensor data or
transforms, so navigation cannot actually run until those exist. Check the
processes from a second terminal (with the workspace sourced):
```bash
ros2 node list
ros2 lifecycle get /controller_server
ros2 lifecycle get /planner_server
```
Both should say `unconfigured`. That only tells us the processes started. It does not
check the controller config, path planning or obstacle avoidance.

You can also launch `nav2.launch.py` directly with `autostart:=false` for the same
navigation-only check. It loads `config/nav2_params.yaml`; use
`params_file:=/absolute/path/to/params.yaml` to point it at a different file.

The main bringup handles mapping, not the navigation launcher:
- `slam:=true` (default) starts one SLAM Toolbox instance.
- `slam:=false map:=/absolute/path/to/map.yaml` starts a map server instead. It
  does not start AMCL, so localization has to line the robot's pose up with the
  saved map. The map has to be aligned to the GPS datum. An arbitrary SLAM map is not
  georeferenced automatically.
- `enable_mapping:=false` starts neither one (for debugging, or when the map comes from somewhere else).

`hardware:=true` is still the default. The motors only start in `follow:=true` mode
(see below), behind the joystick e-stop. `use_sim_time` is passed to navigation and
mapping; leave it false unless something is publishing `/clock`.


## Who owns which transform, and the tests that need no hardware

The main bringup picks the localization from `slam`:

| Mode | `map -> odom` owner | `odom -> base_link` owner |
| --- | --- | --- |
| `slam:=true` | SLAM Toolbox | Local EKF |
| `slam:=false` | GPS/global EKF | Local EKF |

RF2O gives us `/odom_rf2o` without publishing a transform, as long as you use our
launch and config. The upstream RF2O launch file still publishes one, so do not run
that next to the local EKF. Nav2's controller, navigator and velocity smoother use
`/odometry/local`. In GPS mode, `navsat_transform_node` reads its own section of the
YAML and the global EKF combines GPS position with the IMU and RF2O motion.
`enable_mapping:=false` only turns off the map source; it does not change which
localization we use. With `hardware:=false`, no EKFs or sensor drivers start
(unless `sim:=true`, which runs the EKFs on simulated sensors).

Mapping mode on purpose does not run the global GPS EKF or navsat transform.

Run these tests from the workspace root, after building and sourcing:
```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select bring_up
source install/setup.bash

# Real Nav2 with a synthetic map, scan, odometry, and TF:
python src/bring_up/scripts/nav2_smoke_test.py

# Real local EKF driven by synthetic IMU and laser odometry:
python src/bring_up/scripts/nav2_smoke_test.py --localization local

# Both real EKFs and navsat_transform, fed synthetic GPS fixes; also drives the
# robot 10 m and checks /odometry/global and /odometry/gps agree within 0.2 m:
python src/bring_up/scripts/nav2_smoke_test.py --localization gps

# Beacon GPS -> map conversion (beacon_goalpose + navsat /fromLL):
python src/beacon_pkg/scripts/beacon_smoke_test.py

# Full beacon following and return home on a simulated robot (~5 min):
python src/bring_up/scripts/follow_smoke_test.py --beacon-speed 1.2

# Unit tests (drive controller with a fake ODrive, e-stop, GPS monitor, mission logic,
# Meshtastic parsing, ultrasonic stop, BNO085):
python3 -m pytest src/bring_up/test/test_diff_drive_controller.py src/bring_up/test/test_e_stop.py \
  src/bring_up/test/test_gps_monitor.py src/bring_up/test/test_mission_manager.py \
  src/bring_up/test/test_meshtastic_bridge.py src/bring_up/test/test_ultrasonic_estop.py \
  src/bring_up/test/test_bno085_imu.py
```

Each test uses localhost-only ROS domain 87, will not run if that domain is busy, and
cleans up its own processes. Use `--domain-id 88` if you need a different one. Your
normal ROS session can stay running in its own domain. Logs go to
`/tmp/roboflock-nav2-smoke.log` by default; use `--log /tmp/my-test.log` to change
that.

A pass means all seven Nav2 lifecycle nodes go active, a path to `(1, 0)` is found
in the test map, the transform chain and the publishers look right, and the EKF
modes give filtered odometry. The test robot sits still in an empty world. It
does not drive to a goal, and it does not check collision avoidance, tracking
accuracy, SLAM scan matching or the motors.

Before we run on real GPS, we still have to measure and publish the antenna
transform from `base_link` to `gps`, check the IMU mounting and ENU heading, and
set the magnetic declination and yaw offset for where we are testing. The sensor
transforms and GPS coordinates in the tests are fake, not calibration. A saved map
also needs the same datum and orientation every time we start, and the automatic
datum is not saved between runs. All of that still has to be done on the robot even
when the tests pass.


## Following the beacon, and returning home

The robot follows a person (Tom) carrying a GPS beacon, and it can drive back to a
home station that can be moved at any time. Both use the GPS-aligned `map` frame,
so they need `slam:=false`.

```bash
# On the robot (hardware):
ros2 launch bring_up bringup.launch.py follow:=true slam:=false

# Also connect the Meshtastic home station:
# (defaults: meshtastic_port:=/dev/meshtastic home_node_id:=!6c743480)
ros2 launch bring_up bringup.launch.py follow:=true slam:=false station:=true

# Hardware-free simulation (fake robot, sensors and walking beacon; real EKFs and Nav2):
ros2 launch bring_up bringup.launch.py follow:=true slam:=false hardware:=false sim:=true
```

Change mode from the Meshtastic app (as a text message) or from the Jetson:
```bash
ros2 topic pub --once /station/command std_msgs/msg/String "data: home"   # follow | home | stop | status
```

| Piece | What it does |
| --- | --- |
| HC-12 radio (`beacon_receiver.launch.py`) | Beacon GPS NMEA into `/dev/ttyTHS1`, published as `/gps/beacon/fix` |
| `beacon_goalpose` / `home_goalpose` | Convert beacon / home lat-lon to `map` via navsat `/fromLL`; targets over 20 m away are pulled in so they stay on the 50 m rolling costmap |
| `mission_manager` | Modes `idle`, `follow` (stop 3 m short, `follow_beacon.xml`), `home` (stop 1.5 m short, `return_home.xml`); cancels the Nav2 goal when the target goes stale (3 s) or the mode changes; status on `/robot/status` |
| `meshtastic_bridge` (`station:=true`) | Home station positions to `/home/fix`, republished at 1 Hz until 30 min old; text commands to `/station/command`; status back over the mesh |
| `twist_mux` | Nav2 `/cmd_vel` and joystick `/cmd_vel_joy` in (joystick wins); `/cmd_vel_mux` out |
| `ultrasonic_estop` | Takes `/cmd_vel_mux`, blocks forward motion if a front sensor is closer than 0.5 m or has gone quiet, and publishes `/cmd_vel_safe` |
| `e_stop` | PS4 Cross stops, Options arms; losing the joystick for 0.5 s stops. Motors stay idle until armed |
| `diff_drive_controller` | Listens to `/cmd_vel_safe` and drives the ODrives; idles on e-stop, commands zero after 0.5 s without a command, and keeps retrying any ODrive it cannot find |

Nav2 uses Regulated Pure Pursuit at 10 Hz (MPPI was too heavy for the Orin Nano),
up to 1.2 m/s, braking at 1.5 m/s². Acceleration is 0.5 m/s², which matches the
ODrive velocity ramp. As a result the robot lags a steadily walking target and
catches up when the target stops.

### Hardware assignment
- **Robot:** u-blox ZED-F9P (dual-band) on USB (`/dev/ublox_gps`, see
  `config/robot_gps.yaml`), HC-12 receiver on `/dev/ttyTHS1`, Meshtastic node on USB.
- **Beacon (Tom):** NEO-M8P sending NMEA GGA at 9600 baud into the HC-12 transmitter.
  Wiring: NEO-M8P UART1 TX to HC-12 RXD, shared GND, and 5 V from a power bank to
  the NEO-M8P's USB and the HC-12 VCC. Leave HC-12 SET unconnected (factory
  defaults: 9600 baud, channel 001, FU3, same as the robot's HC-12). Set up the
  NEO-M8P once over USB (UART1: GGA only, 5 Hz, saved to flash):
  `python3 src/beacon_pkg/scripts/configure_beacon_gps.py /dev/ttyACM<n>`
  (`--check` just verifies it).
  Tom also carries a Meshtastic handheld paired with their phone, for commands.
- **Home station:** a Meshtastic node with GPS on, smart position broadcast on, and
  channel position precision at 32 bits (lower precision rounds the position off).
- **Meshtastic radios** (LILYGO T-Beams, all role CLIENT):

  | Label | Node | Use |
  | --- | --- | --- |
  | ROBT | `!6c73d700` | Robot, USB to the Jetson (`/dev/meshtastic`), GPS off |
  | HOME | `!6c743480` | Home station, GPS on, smart broadcast |
  | TOM | `!bb80e074` | Tom's handheld, paired with the phone app; allowed to send commands |

  Channel 0 on all three is the private `roboflock` channel (position precision
  32). Its key lives on the Jetson in `~/.config/roboflock/meshtastic_primary_psk.b64`
  and is not in git. Channel 1, `fromJetson`, carries the robot's status.
- The Python `meshtastic` library comes from PyPI (`pip install --user meshtastic==2.7.11`).

### IMU: no compass yet
The IMU on the robot is an **MPU-6050** (WHO_AM_I `0x68`), not an MPU-9250. It has
no magnetometer, so `mpu9250driver` publishes a fixed yaw (about -135°) and logs
`Remote I/O error` on every compass read. GPS localization gets its absolute heading
from the IMU, so **do not trust GPS localization or follow mode until a BNO085 is
installed**.

- Wiring (either board): VCC to **3.3 V** (pin 1, not 5 V), GND to pin 6, SDA to pin
  27, SCL to pin 28 (`/dev/i2c-1`). Mount it flat, with X forward and Y left.
- The BNO085 code is written but we have not tested it on hardware
  (`bring_up/bno085_imu.py`; the chip fuses the magnetometer itself). Install its
  libraries, then select it:
  ```bash
  pip install --user adafruit-circuitpython-bno08x adafruit-extended-bus
  ros2 launch bring_up bringup.launch.py follow:=true slam:=false imu:=bno085
  ```
  Check that it answers at `0x4A` with `i2cdetect -y -r 1`. Outside, point the robot
  east and then north, and set navsat's `yaw_offset` and
  `magnetic_declination_radians` in `config/ekf_navsat_params.yaml` so east reads 0.
- `mpu9250driver` calibrates at startup by assuming it is level, so it cannot show a
  mounting tilt, and it keeps publishing even if the sensor stops answering.

### Known issue: tf2 deadlock
On Humble (`tf2_ros` 0.25.23), a lidar scan stamped ahead of the TF data can
deadlock Nav2's costmap TF listener (`MessageFilter` vs `testTransformableRequests`).
The controller then freezes with "extrapolation into the future" errors. The
simulated lidar stamps scans 0.1 s in the past, like `rplidar_ros`. If the real
robot freezes like this, look at the lidar's scan timestamps first.

### Hardware commissioning checklist
1. `sudo usermod -aG dialout roboflock` (serial ports), then install the udev
   rules for `/dev/ublox_gps`, `/dev/rplidar_usb`, `/dev/meshtastic` and the PS4 controller:
   `sudo cp src/bring_up/udev/99-roboflock.rules /etc/udev/rules.d/ && sudo udevadm control --reload-rules && sudo udevadm trigger`.
   Use a data USB-C cable for the ZED-F9P. With a charge-only cable the board
   powers up but never shows up.
2. Check that the ZED-F9P has a dual-band (L1/L2) antenna.
3. GPS antenna offset is measured (0.16 m forward, 0.63 m above ground) and set in
   the URDF. The MPU-6050 is wired to `/dev/i2c-1` but not mounted, and it has no
   compass. Install a BNO085 (see "IMU: no compass yet"), mount it, then check ENU
   heading and set the magnetic declination.
4. With the wheels raised, test the e-stop (Cross, Options, unplugging the
   joystick), 1.5 m/s² braking, and the stale `/cmd_vel` watchdog.
5. Stationary GPS: log `/odometry/global` for 5 minutes and measure the drift.
6. Set up the Meshtastic radios (see Hardware assignment). Tom's phone is paired
   with TOM, and `status` and `stop` make the round trip to the robot. Still to do:
   get a home position from HOME outdoors.
7. Open field: the walker stays at least 10 m ahead, and a spotter holds the PS4
   controller.

### Motor power

Before you connect the motor battery, read `docs/project/electrical_review.rst`
(on the docs site under Project). The motor controllers are 24 V boards with 30 V
transistors and the pack charges to 29.4 V. The only way to cut motor power is to
unplug the battery. `roboflock-drive.service` is turned off on the robot because
it connects to the controllers and arms on one button press.
