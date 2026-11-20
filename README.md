# RoboFleet - Autonomous Mobile Robot (ROS 2)

**RoboFleet** is the University at Buffalo team's 2026–2027 continuation of the inherited **RoboFlock** rover. This year's required deliverable is **one FleetBot** that follows a GPS **RoboBeacon** with obstacle-aware navigation, an operator stop, and supervised light-rain/dust protection.

**[ReadTheDocs | Official Project Documentation](https://robofleet.readthedocs.io/en/latest/)** · **[DeepWiki | Interactive Code Exploration](https://deepwiki.com/ryantcliff/robofleet_ws/)**

ReadTheDocs is the maintained documentation website. DeepWiki is an automatically generated, complementary way to explore code and should be checked against the repository and ReadTheDocs.

> **Project continuity:** Historical ROS, configuration, and device identifiers may still say `roboflock`. We preserve them until there is a tested reason to rename them.

## The Platform

- **ROS 2 Humble** on NVIDIA Jetson Orin Nano with Nav2, SLAM Toolbox, `robot_localization`, LiDAR and u-blox GPS.
- GPS beacon-to-goal and safety-control software exists, but simulation success is **not** an outdoor hardware acceptance test.
- Four inherited ODESC motor controllers; **motor-battery voltage margin and physical motor-power cutoff remain unresolved**. [Read the electrical review](https://robofleet.readthedocs.io/en/latest/project/electrical_review.html) before powered work.
- BNO085 absolute-heading IMU and RPLIDAR S2 are **planned**, not installed. Meshtastic/return-home functions are inherited and optional this year.
- Environmental requirement: supervised light rain, incidental splashes and wind-blown alkaline dust. No full-robot IP rating is claimed.

## Architecture and Demonstration

[![Repository architecture diagram](https://gitdiagram.com/ryantcliff/robofleet_ws/diagram.png)](https://gitdiagram.com/ryantcliff/robofleet_ws?utm_source=readme&utm_medium=picture)

[Watch the inherited FleetBot SLAM demonstration](https://github.com/user-attachments/assets/d75cb297-7618-43ef-b84b-9466528e4aed).

## Build

The ROS 2 packages, launch files and configurations are in `src/`. Detailed installation and hardware procedures are maintained in ReadTheDocs.

~~~bash
source /opt/ros/humble/setup.bash
cd ~/robofleet_ws
rosdep install --from-path src --rosdistro humble -y
colcon build --symlink-install --executor sequential
source install/setup.bash
~~~

The inherited Jetson clone may still be located at `~/roboflock_ws`; use the existing directory if so. A successful build is **not** evidence that the physical robot is safe to drive.

## Documentation Map

- [Getting Started / Launch Options](https://robofleet.readthedocs.io/en/latest/getting_started/installation.html)
- [Navigation, GPS and TF](https://robofleet.readthedocs.io/en/latest/concepts/navigation.html) · [Control and Safety](https://robofleet.readthedocs.io/en/latest/concepts/control_safety.html)
- [Beacon Following](https://robofleet.readthedocs.io/en/latest/concepts/beacon_following.html) · [Communications](https://robofleet.readthedocs.io/en/latest/concepts/communications.html)
- [Navigation-Only Debugging](https://robofleet.readthedocs.io/en/latest/tutorials/navigation_debugging.html) · [Simulation and Unit Tests](https://robofleet.readthedocs.io/en/latest/tutorials/simulation.html)
- [Hardware Commissioning](https://robofleet.readthedocs.io/en/latest/tutorials/commissioning.html) · [Troubleshooting](https://robofleet.readthedocs.io/en/latest/tutorials/troubleshooting.html)
- [Hardware Inventory](https://robofleet.readthedocs.io/en/latest/project/hardware_inventory.html) · [Requirements](https://robofleet.readthedocs.io/en/latest/project/requirements.html)
