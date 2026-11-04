Roadmap & Status
================

Where each piece of the project stands. We do not mark something done until it
has been tested on the robot. What we owe is one working FleetBot.

.. list-table::
   :header-rows: 1
   :widths: 35 28 37

   * - Work item
     - Status
     - What is next
   * - Inherited ROS 2 / Nav2 baseline
     - :ready:`Audited / software tests present`
     - Repeat on the final robot image
   * - RoboBeacon reception
     - :ready:`Integration path present`
     - Outdoor test: valid fixes become goals
   * - Beacon-follow distance
     - :ready:`Current target is 3 m`
     - Open-field test with a moving beacon; check we land in 1.5-3.0 m
   * - Beacon-loss stop
     - :ready:`Logic present`
     - Cut the RoboBeacon updates and check it stops
   * - Drive stack startup and sonar backup
     - :ready:`Fixed and unit tested`
     - Replug the Arduino and a motor controller on the robot
   * - BNO085 absolute heading
     - :planned:`Required hardware upgrade`
     - Detect it on I2C, check axes, calibrate, test a known direction
   * - RPLIDAR S2 30 m (IP65)
     - :planned:`Planned purchase and integration`
     - Update baud and udev, check ``/scan`` and obstacle behavior
   * - Motor power safety
     - :planned:`In progress`
     - See :doc:`electrical_review`: voltage margin, a real stop, braking test
   * - Weather protection
     - :planned:`Formal requirement`
     - Light-rain / splash and alkaline-dust checks, plus a heat check
   * - RoboBeacon as a carried object
     - :planned:`No enclosure, power or indicators yet`
     - Agree requirements with Tom, measure accuracy and range, then design the case.
       See :doc:`robobeacon_plan`
   * - Burning Man environment
     - :planned:`Researched, not yet checked with the client`
     - Raise licensing, radio limits and storm handling with Tom. See :doc:`burning_man`
   * - Full outdoor demo
     - :planned:`Final integration`
     - Follow, obstacle awareness, e-stop and handoff documentation

Schedule
--------

We plan to finish integration and documentation in March 2027. Final delivery
is **no later than April 1, 2027**, per the requirements document.

Beyond this year
----------------

RoboFleet is meant to grow into many FleetBots that know about each other and plan
around each other. That is not part of what we owe this year. We keep it in mind so
that we do not make it harder, for example by avoiding new fixed topic names. See
:doc:`burning_man`.

Keeping these docs honest
-------------------------

When we change hardware, we update these pages, the repo config, and the wiring
and URDF records together, so the next team gets one consistent picture.
