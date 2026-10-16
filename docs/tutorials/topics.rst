ROS Topics & Interfaces
=======================

Key ROS interfaces used by the current integration are summarized below.

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - Topic
     - Type / role
   * - ``/scan``
     - LiDAR ``sensor_msgs/LaserScan``
   * - ``/imu/data``
     - IMU orientation, angular velocity, and acceleration
   * - ``/gps/robot/fix``
     - Robot GNSS fix
   * - ``/gps/beacon/fix``
     - Beacon GNSS fix received by the robot
   * - ``/odom_rf2o``
     - Laser odometry input
   * - ``/odometry/local``
     - Local EKF result used by Nav2
   * - ``/odometry/global``
     - GPS-aligned global EKF result
   * - ``/cmd_vel``
     - Nav2 velocity output
   * - ``/cmd_vel_joy``
     - Joystick command path
   * - ``/cmd_vel_estop``
     - Ultrasonic emergency-stop command path
   * - ``/cmd_vel_mux``
     - Arbitrated velocity command to motor controller
   * - ``/station/command``
     - Follow/home/stop/status mode command
   * - ``/robot/status``
     - Robot status for telemetry

Useful inspection commands
--------------------------

.. code-block:: bash

   ros2 topic list
   ros2 topic info /scan
   ros2 topic echo /imu/data --once
   ros2 run tf2_ros tf2_echo map base_link
   ros2 node list
