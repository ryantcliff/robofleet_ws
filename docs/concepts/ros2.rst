ROS 2 Architecture
==================

ROS 2 is what ties everything together. Sensors publish standard messages,
localization combines them, Nav2 plans the motion, and a few safety nodes
decide what velocity the motors actually get.

Data path
---------

::

   /scan -----------+
   /imu/data -------+--> RF2O + EKFs --> TF + odometry --> Nav2
   /gps/robot/fix --+                                  |
                                                       v
                                                  /cmd_vel
                                                       |
                                                       v
                                                   twist_mux  <-- /cmd_vel_joy (PS4)
                                                       |
                                                       v
                                                 /cmd_vel_mux
                                                       |
                                                       v
                                       ultrasonic_estop (blocks forward motion)
                                                       |
                                                       v
                                                 /cmd_vel_safe
                                                       |
                                                       v
                                          diff_drive_controller --> 4 ODrives

``twist_mux`` picks between Nav2 and the joystick (the joystick wins).
``ultrasonic_estop`` sits after it, so it can stop forward motion no matter
where the command came from. ``e_stop`` is separate: it publishes an armed or
stopped flag that ``diff_drive_controller`` watches.

Transform ownership
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Mode
     - Who owns ``map -> odom``
     - Who owns ``odom -> base_link``
   * - Mapping
     - SLAM Toolbox
     - Local EKF
   * - GPS localization
     - Global EKF / navsat
     - Local EKF

.. important:: One owner per transform

   Only one node should publish each transform. RF2O should give us laser
   odometry without also publishing the transform the local EKF owns.
