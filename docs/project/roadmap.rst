Roadmap & Status
================

This page tracks the 2026-2027 engineering direction without implying
completion before hardware validation. The formal acceptance target is one
working FleetBot.

.. list-table::
   :header-rows: 1
   :widths: 35 28 37

   * - Work item
     - Status
     - Next validation
   * - Inherited ROS 2/Nav2 baseline
     - :ready:`Audited / software tests present`
     - Repeat on final hardware image
   * - RoboBeacon reception
     - :ready:`Integration path present`
     - Outdoor valid-fix and goal-conversion test
   * - Beacon-follow stand-off
     - :ready:`Current target is 3 m`
     - Open-field moving-beacon test; verify 1.5-3.0 m acceptance range
   * - Beacon-loss fail-safe
     - :ready:`Logic present`
     - Stop/cancel test with RoboBeacon updates removed
   * - BNO085 absolute heading
     - :planned:`Required hardware upgrade`
     - I2C detection, axis check, magnetic calibration, known-direction test
   * - RPLIDAR S2 30 m (IP65)
     - :planned:`Planned purchase / integration`
     - Update baud/udev settings and verify ``/scan`` + obstacle behavior
   * - Weather protection
     - :planned:`Formal requirement`
     - Controlled light-rain/splash and alkaline-dust inspection; thermal check
   * - Full required outdoor demo
     - :planned:`Final integration`
     - RoboBeacon follow, obstacle awareness, e-stop, and documentation handoff

Schedule target
---------------

The team plans to complete final integration and documentation during March
2027, with final delivery **no later than April 1, 2027** under the current
requirements-document schedule.

Documentation policy
--------------------

When a hardware change is made, update this site, repository configuration, and
the physical wiring/URDF records together so the next team inherits one
consistent source of truth.
