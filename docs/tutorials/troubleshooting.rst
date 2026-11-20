Troubleshooting and known issues
================================

Use this page for symptoms, evidence and safe first diagnostics. A hypothesis
is not the same as a confirmed root cause.

Nav2 appears frozen; TF extrapolation
-------------------------------------

A previously observed **possible** ROS 2 Humble / tf2 interaction
(reported against ``tf2_ros`` 0.25.23) involves lidar scans timestamped
ahead of available transforms. Symptoms include costmap warnings about
"extrapolation into the future" and navigation updates stopping.

There has been a suspected ``MessageFilter`` / ``testTransformableRequests``
deadlock in this setup, but a matching warning by itself is **not**
conclusive proof of a deadlock.

Start with non-invasive checks:

.. code-block:: bash

   ros2 topic echo /scan --once
   ros2 topic hz /scan
   ros2 run tf2_ros tf2_echo odom base_link
   ros2 node list

Compare ``/scan`` header timestamps, the ROS clock source, and available TF
timestamps. Verify ``use_sim_time`` versus actual ``/clock`` configuration.
Do not force timestamps backward just to hide an error; determine the
source of clock/driver delay first. The simulation has historically
timestamped fake lidar scans around 0.1 s in the past, which should not
be treated as a real-driver fix.

GPS follows the wrong direction
-------------------------------

The inherited MPU-6050 has no magnetometer and the legacy driver supplies
fixed yaw. GPS heading cannot be trusted with this configuration. A BNO085
is required and remains unverified on physical hardware. Check placement,
I2C detection, ENU yaw, yaw offset and local magnetic declination before
allowing outdoor follow mode. See :doc:`../concepts/navigation`.

Ultrasonic failsafe not guarding
--------------------------------

Confirm the real Arduino shows up, its serial publisher is running,
the three sonar topics are fresh, and ``ultrasonic_estop`` is in
fail-closed mode. The brake never acts while the PS4 controller is driving, so test
it with Nav2 or follow commands. A ROS test with fake sensor data is not a substitute
for unplug/replug and obstacle tests. See
:doc:`../concepts/obstacle_detection`.

Motor controllers not enumerated
--------------------------------

The inherited four controllers historically enumerated over USB only
with the motor battery connected. **Do not connect the battery solely
to investigate enumeration.** Review :doc:`../project/electrical_review`
and existing diagnostic evidence in :doc:`../project/jetson_diagnostics`.
Do not clear faults or change firmware/configuration as a diagnostic
first step.

One-pin nets in converted NVIDIA reference schematic
-----------------------------------------------------

The Altium import of NVIDIA's Jetson P3768 carrier-board OrCAD base
schematic has numerous unused/reserved-pin ERC messages. Its Concept PDF,
OrCAD base PDF and assembly/BOM files should be used as a comparison
before renaming nets, suppressing warnings, or changing wiring. This is
an external reference schematic, **not** the FleetBot's own schematic.
