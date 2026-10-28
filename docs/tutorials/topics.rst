ROS Topics & Interfaces
=======================

The main topics we use:

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - Topic
     - What it is
   * - ``/scan``
     - LiDAR scan (``sensor_msgs/LaserScan``)
   * - ``/imu/data``
     - IMU orientation, angular velocity and acceleration
   * - ``/gps/robot/fix``
     - The robot's GPS fix
   * - ``/gps/beacon/fix``
     - The RoboBeacon's GPS fix, as received by the robot
   * - ``/odom_rf2o``
     - Laser odometry
   * - ``/odometry/local``
     - Local EKF output, used by Nav2
   * - ``/odometry/global``
     - GPS-aligned global EKF output
   * - ``/cmd_vel``
     - Nav2's velocity command
   * - ``/cmd_vel_joy``
     - Joystick velocity command
   * - ``/cmd_vel_mux``
     - What ``twist_mux`` picked (joystick wins over Nav2)
   * - ``/cmd_vel_safe``
     - ``/cmd_vel_mux`` after ``ultrasonic_estop`` has blocked forward motion if
       needed. This is what the motor controller listens to.
   * - ``/e_stop``
     - Armed / stopped flag from ``e_stop``
   * - ``/range/left_ultrasonic``, ``center``, ``right``
     - Ultrasonic distances
   * - ``/station/command``
     - Mode command: follow, home, stop or status
   * - ``/robot/status``
     - Robot status for telemetry

Useful commands
---------------

.. code-block:: bash

   ros2 topic list
   ros2 topic info /scan
   ros2 topic echo /imu/data --once
   ros2 run tf2_ros tf2_echo map base_link
   ros2 node list
