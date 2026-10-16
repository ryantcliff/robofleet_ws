Roadmap & Status
================

This page tracks the current-year engineering direction without implying
completion before hardware validation.

.. list-table::
   :header-rows: 1
   :widths: 35 28 37

   * - Work item
     - Status
     - Next validation
   * - Inherited ROS 2/Nav2 stack audit
     - :ready:`In progress / validated in software`
     - Repeat on final hardware image
   * - Beacon-following software
     - :ready:`Integration path present`
     - Open-field hardware test
   * - BNO085 absolute heading
     - :planned:`Planned hardware`
     - I2C detection, axis check, magnetic calibration
   * - IP-rated RPLIDAR
     - :planned:`Planned purchase`
     - Update baud/udev settings and verify ``/scan``
   * - Weatherproof electronics
     - :planned:`Design requirement`
     - Enclosure and controlled spray test
   * - Full autonomous follow demo
     - :planned:`Final integration`
     - Outdoor acceptance test with spotter

Documentation policy
--------------------

When a hardware change is made, update this site, the repository configuration,
and the physical wiring/URDF records together so the next team inherits one
consistent source of truth.
