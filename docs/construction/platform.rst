Inherited Platform
==================

RoboFleet inherits the mechanical rover from the previous RoboFlock team. The
current team should preserve working mechanical subsystems unless a change is
required for reliability, weatherproofing, serviceability, or sensor mounting.

Inherited assemblies
--------------------

**Chassis**
   Main structural frame and extrusion rails.

**Drive system**
   Four BLDC drive corners controlled as a differential/skid-steer platform.

**Wheels & suspension**
   Airless wheels with passive rocker-differential suspension.

**Hull & electronics**
   Protective body, compute, sensor mounts, power distribution, and wiring.

Change-control rule
-------------------

Before modifying inherited geometry, record the original dimensions, mounting
position, connector routing, and corresponding URDF transform. Mechanical
changes that move GPS, IMU, or LiDAR sensors must be reflected in TF/URDF
configuration.
