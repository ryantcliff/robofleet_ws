Hardware verification checklist
===============================

Our to-do list for checking the hardware. Start with everything powered off.
Do not open the lithium packs. The motor power items below are worked out in
detail on :doc:`electrical_review`, which has what we measured and what we
found.

Priority 0: motor power
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Item
     - Where it stands
   * - Controllers vs. battery
     - All four ODESC V4.2 controllers are identical. The one we looked at (RL)
       has JMTG3002B power MOSFETs rated 30 V absolute maximum and a 24 V QC
       marking, and our 7S pack charges to 29.4 V. That is too close, because
       switching spikes and braking push the bus voltage up. We have not fixed
       this. Details and what we have tried are on :doc:`electrical_review`.
   * - Braking resistors
     - Done. All four are connected and read 2 ohm. The controllers are now set
       to use them (2.0 ohm, enabled).
   * - Battery power path
     - Visual inspection complete. Four 20 A fuses on the motor controllers, one 5 A fuse on
       the Jetson, no main fuse, 10 AWG wire with correct polarity and no
       damage. There is no master disconnect.
   * - Motor safety stop
     - We do not have a physical one. Unplugging the battery is the only way to
       cut motor power. The software e-stop (PS4 Cross) idles the motors and
       they coast. Test it with the wheels off the ground.
   * - Wheel retention
     - Not done. Check the hub, clamp, shaft key and set screws, the bearings,
       and how much of the load the gearbox shaft carries.

Priority 1: electronics
-----------------------

* Measure the Jetson's power supply setting and the 3S battery's voltage range
  under load. The LM2596 only steps voltage down.
* Find out exactly which USB hub model is which, and which port goes where.
  Unplug and replug things and check they come back with the same serial.
* Check the Arduino Nano firmware, which ultrasonic board is which, the
  connector pinout and the sensor directions.
* Check the ZED-F9P antenna path, correction source, fix type and GPS
  covariance. Log the position while it sits still before we trust GPS
  following.
* Check the RoboBeacon NEO-M8P-2 / HC-12 link and what happens when its data
  stops. The HC-12 pinout is normally VCC, GND, RXD, TXD, SET; check the
  silkscreen before wiring.
* Install and test the BNO085 for a real absolute heading before using
  GPS-based navigation.
* Test the RPLIDAR A1M8 we have. We only call the S2 installed once it is bought
  and working.

Priority 2: geometry, weather, repeatability
--------------------------------------------

* Measure the wheelbase, track width, loaded wheel radius, tire pressure,
  ground clearance, frame size, total mass and center of mass.
* Write down the extrusion profiles, brackets, motor mounts, 3D-printed part
  materials, fasteners and drivetrain couplers.
* Plan the enclosure and cable glands for light rain, splashes and alkaline
  dust. We do not give the whole robot an IP rating without testing it.
* Decide whether the Surface Go 2 and HOME T-Beam are part of a home-base
  prototype. They are optional right now.

For each item we finish, write down the date, who did it, the instrument or
photo, the measurement, and whether it passed. We do not mark something
"commissioned" just because it looks fine.
