Navigation & Localization
=========================

We use two localization modes. In mapping mode the robot builds a SLAM map. In
follow or home mode it uses GPS-aligned localization, so a latitude and
longitude can become a Nav2 goal.

Local odometry
--------------

RF2O gives us laser odometry on ``/odom_rf2o``. The local EKF combines that
with the IMU, publishes ``/odometry/local``, and owns ``odom -> base_link``.

Global GPS localization
-----------------------

In GPS mode, ``navsat_transform_node`` and the global EKF combine the robot's
GPS, the IMU heading and the local motion into a global pose. We use that for
the beacon and home targets.

Why we need a better IMU
------------------------

GPS localization needs an absolute heading, and our old MPU-6050 has no
magnetometer. The current code includes a BNO085 driver so we can use the
fused magnetic heading once the board is installed and calibrated.

.. warning:: Calibrate outdoors

   After mounting the BNO085, check the axis directions, the magnetic
   declination and ``yaw_offset`` outside before trusting autonomous GPS
   navigation.
