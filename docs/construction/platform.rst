Inherited Platform
==================

The mechanical rover comes from the previous RoboFlock team. We keep what
works and only change something when it helps reliability, weatherproofing,
serviceability or sensor mounting.

What we inherited
-----------------

**Chassis**
   Aluminum T-slot extrusion frame.

**Drive system**
   Four BLDC motors, one per corner, driven as a skid-steer (differential)
   platform.

**Wheels**
   Four pneumatic tires (4.10/3.50-4) on metal rims. An earlier note called
   them nylon, but they are not.

**Body and electronics**
   An open-topped electronics tray, compute, sensor mounts, power distribution
   and wiring.

Before you change the geometry
------------------------------

Write down the original dimensions, mounting position, connector routing and
the matching URDF transform first. If a change moves the GPS, IMU or LiDAR, the
TF/URDF config has to be updated to match.
