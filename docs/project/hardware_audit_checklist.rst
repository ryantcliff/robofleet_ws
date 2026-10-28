Hardware verification checklist
===============================

This is an inspection plan, **not** permission to energize an unverified
motor controller or open lithium battery packs. Start de-energized, and
have a qualified supervisor review battery and power-stage tests.

Priority 0 — before reconnecting motor power
--------------------------------------------

.. list-table::
   :header-rows: 1

   * - Item
     - Evidence needed
   * - ODESC FL, FR, RL and RR rated input voltage
     - Part/purchase documentation and board component identification;
       compare maximum rated bus voltage with fully charged 7S = 29.4 V
       and expected regeneration/transients
   * - Braking resistors
     - Check each labeled 50W 2RJ component's continuity, terminal
       assignment, firmware resistance setting, and metal heatsinking
   * - Battery power path
     - Label each fuse rating, wire size and polarity; verify safe
       master disconnect, strain relief, connectors and insulation
   * - Motor safety stop
     - Identify physical stopping hardware and separately validate
       the existing software e-stop/watchdog with wheels safely raised
   * - Mechanical wheel retention
     - Identify wheel hub, clamp, shaft key/set screws, independent
       bearings and gearbox shaft radial/bending load

Priority 1 — electronics bring-up
---------------------------------

* Measure Jetson power supply setting and battery voltage ranges under
  controlled, supervised loading; LM2596 is a buck-only converter.
* Identify the exact USB hub model and upstream ports. Inspect
  disconnected/reconnected device enumeration and serial identity.
* Confirm Arduino Nano firmware, three ultrasonic board identities,
  connector pinout, obstacle/timeout failsafe and sensor orientations.
* Verify ZED-F9P antenna path, correction source, fix type, GNSS covariance
  and stationary-position variation before GPS following.
* Verify the RoboBeacon NEO-M8P-2/HC-12 telemetry channel and stale-data
  stop behavior. HC-12 physical pinout is conventionally VCC, GND, RXD,
  TXD, SET; check silkscreen before wiring.
* Install and validate the required BNO085-class IMU for true absolute
  heading before enabling GPS-based navigation.
* Test the existing RPLIDAR A1M8; only describe S2 as installed after
  hardware has been purchased and commissioned.

Priority 2 — geometry, environment, reproducibility
----------------------------------------------------

* Measure wheelbase, wheel-center track, loaded rolling radius, tire
  pressure, ground clearance, frame dimensions, total mass and center
  of mass.
* Record aluminum extrusion profiles, corner brackets, motor mounting
  dimensions, printed part materials, fasteners and drivetrain couplers.
* Create an enclosure/cable-gland layout protecting electronics from
  supervised light rain, splash and alkaline dust. Do not assign a
  whole-robot IP rating without testing.
* Determine whether the Surface Go 2 and HOME T-Beam are part of a
  future home-base prototype; optional under the current requirements.
* Keep raw photo identifiers, device serial numbers, Windows IDs and
  private radio/security configuration in a separate private register.

Document each verified item with date, tester, instrument or photograph,
measurement and pass/fail outcome. Do not change a status from
'unverified' to 'commissioned' based on appearance alone.
