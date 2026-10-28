Requirements
============

These come from our 2026-2027 RoboFleet requirements document, which sets our
scope. We build on the inherited RoboFlock platform. We are responsible for
finishing, testing and improving it, and we are not passing off the inherited
parts as new work.

We have to deliver **one working FleetBot**. Multiple FleetBots working
together is part of the bigger RoboFleet idea, but it is not required this year.

Formal requirements
-------------------

.. list-table::
   :header-rows: 1
   :widths: 8 20 36 36

   * - ID
     - Requirement
     - Promise
     - Acceptance / verification
   * - R-1
     - Beacon Position Reception
     - The FleetBot shall receive and use position updates from the RoboBeacon
       while operating in follow mode.
     - Valid beacon fixes are received and converted into navigation goals
       during outdoor testing.
   * - R-2
     - Beacon Following and Target Stand-off
     - When follow mode is active and GPS localization is valid, the FleetBot
       shall autonomously navigate toward the RoboBeacon and stop approximately
       1.5-3.0 m short of the RoboBeacon.
     - In an open-field demonstration, the FleetBot follows a moving RoboBeacon
       and settles near the 1.5-3.0 m target distance without intentional contact.
   * - R-3
     - Beacon-loss Fail-safe
     - The FleetBot shall cancel or stop pursuit when RoboBeacon position data
       becomes stale or unavailable.
     - Removing or stopping RoboBeacon updates cancels the active follow goal
       and stops commanded FleetBot motion.
   * - R-4
     - Obstacle-aware Navigation
     - The FleetBot shall continue to use the current LiDAR/navigation stack to
       avoid known obstacles while actively pursuing the RoboBeacon.
     - A controlled obstacle is represented in the navigation stack and the
       FleetBot does not intentionally drive through it.
   * - R-5
     - Absolute Heading for GPS Localization
     - The FleetBot shall use a magnetometer-capable IMU so GPS localization is
       not dependent on the inherited MPU-6050 fixed-yaw behavior.
     - A BNO085-class IMU is detected, publishes fused orientation on
       ``/imu/data``, and produces directionally consistent heading in known
       orientations.
   * - R-6
     - Weather Protection
     - Critical components and exposed connections shall be protected for
       supervised outdoor operation in light rain, incidental splashes, and
       wind carrying alkaline dust.
     - Visual inspection plus controlled environmental testing confirms the
       protected components/connections remain functional. This is not a claim
       of a complete-robot IP rating, immersion resistance, or unattended severe-weather operation.
   * - R-7
     - Operator Safety Stop
     - The operator shall have a rapid means to stop FleetBot motion during
       testing and demonstrations.
     - The inherited e-stop/arming path is demonstrated before autonomous field
       testing; loss of a valid motion command results in zero commanded velocity.
   * - R-8
     - Documentation and Handoff
     - Current-team changes shall be version-controlled and documented so a
       future team can reproduce the setup and testing procedure.
     - GitHub and Read the Docs contain updated launch/configuration
       instructions, hardware notes, test procedures, and known limitations at
       final delivery.

Key constraints
---------------

* We keep the Jetson Orin Nano / Ubuntu 22.04 / ROS 2 Humble setup. A computer
  upgrade is not in the budget.
* We reuse inherited hardware where we can, and spend effort on the upgrades we
  need for reliability: a BNO085-class heading sensor, an IP-rated LiDAR, and
  weather protection.
* GPS acceptance tests need a clear view of the sky.
* We do not promise the whole robot meets an IP rating.
* Required work comes before optional extras like return-home, Meshtastic and
  extra autonomy.
