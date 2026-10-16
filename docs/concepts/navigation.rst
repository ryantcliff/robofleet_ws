Navigation & Localization
=========================

RoboFleet uses two localization modes. Mapping mode builds a local SLAM map.
Follow/home mode uses GPS-aligned localization so geographic targets can become
Nav2 goals.

Local odometry
--------------

RF2O provides laser odometry on ``/odom_rf2o``. The local EKF combines motion
information with IMU data and publishes ``/odometry/local`` while owning
``odom -> base_link``.

Global GPS localization
-----------------------

In GPS mode, ``navsat_transform_node`` and the global EKF combine robot GNSS,
IMU heading, and local motion to produce a global pose used for geographic
beacon and home targets.

IMU heading requirement
-----------------------

Absolute heading is critical. The inherited MPU-6050 has no magnetometer. The
current branch therefore includes a BNO085 driver so the robot can use fused
magnetic heading after calibration.

.. warning:: Field calibration required

   After mounting the BNO085, verify axis orientation, magnetic declination,
   and ``yaw_offset`` outdoors before trusting autonomous GPS navigation.
