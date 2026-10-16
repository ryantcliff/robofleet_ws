ROS 2 Architecture
==================

ROS 2 is the integration layer for RoboFleet. Sensors publish standard
messages, localization fuses them, Nav2 plans motion, and safety nodes
arbitrate the final motor command.

Core data path
--------------

::

   /scan -----------+
   /imu/data -------+--> RF2O + EKFs --> TF + odometry --> Nav2
   /gps/robot/fix --+                                  |
                                                       v
                                                  /cmd_vel
                                                       |
                                                       v
                                             twist_mux / e-stop
                                                       |
                                                       v
                                                motor controller

TF ownership
------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Operating mode
     - ``map -> odom`` owner
     - ``odom -> base_link`` owner
   * - Mapping
     - SLAM Toolbox
     - Local EKF
   * - GPS localization
     - Global EKF / navsat pipeline
     - Local EKF

.. important:: Single owner per transform

   RF2O should provide laser odometry without also publishing the same TF that
   the local EKF owns.
