Navigation-only debugging (no robot hardware)
=============================================

This launches Nav2 processes without motor controllers, sensor drivers or fake
sensor data. It is a **startup check**, not a path-following, obstacle avoidance,
or physical safety test. For simulated-sensor tests, see :doc:`simulation`.

Install and build
-----------------

On Ubuntu 22.04 / ROS 2 Humble, install packages if missing:

.. code-block:: bash

   sudo apt-get install ros-humble-navigation2 ros-humble-nav2-bringup \
     ros-humble-slam-toolbox ros-humble-robot-localization

From the actual workspace root (it may still be named `~/roboflock_ws` on
the inherited Jetson):

.. code-block:: bash

   source /opt/ros/humble/setup.bash
   cd ~/robofleet_ws
   colcon build --packages-select bring_up
   source install/setup.bash

Launch Nav2 without hardware
----------------------------

.. code-block:: bash

   ros2 launch bring_up bringup.launch.py \
     hardware:=false enable_mapping:=false autostart:=false

This does **not** start real sensor drivers, GPS, IMU, localization EKFs, the
robot state publisher, the beacon, or the motor controller. Nothing publishes
synthetic sensor or transform data in this mode.

Open a second sourced terminal:

.. code-block:: bash

   ros2 node list
   ros2 lifecycle get /controller_server
   ros2 lifecycle get /planner_server

The latter two should report `unconfigured` if their processes started.
This does **not** verify that they can plan or control a robot.

Direct navigation launch
------------------------

An equivalent navigation-server-only check is:

.. code-block:: bash

   ros2 launch bring_up nav2.launch.py autostart:=false

It loads `config/nav2_params.yaml`. Override with
`params_file:=/absolute/path/to/params.yaml` if required.

Understanding map and localization flags
----------------------------------------

* `slam:=true` with mapping enabled starts SLAM Toolbox.
* `slam:=false map:=/absolute/path/to/map.yaml` with mapping enabled
  loads a saved map, unless the follow-mode rolling-costmap path is selected.
  This does **not** start AMCL; an arbitrary saved SLAM map does not have
  a GPS datum and orientation automatically.
* `enable_mapping:=false` selects neither SLAM nor the saved-map server.
* `hardware:=false sim:=true` runs the separately implemented simulated
  robot / localization path. It is **not** the same as navigation-only mode.
* `use_sim_time` should remain false unless a source is publishing `/clock`.
* `follow:=true` requires `slam:=false` and, on real hardware, starts a
  motor-control stack. Do not use it as a harmless debugging substitute.

A complete synthetic test exercises more components; see :doc:`simulation`.
