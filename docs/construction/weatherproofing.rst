Weatherproofing
===============

Weather protection is a formal current-year requirement. The objective is to
protect critical components and exposed connections during **supervised
outdoor use in light rain, incidental splashes, and wind carrying alkaline
dust**.

This requirement deliberately does **not** claim that the complete FleetBot is
IP-rated, submersible, suitable for unattended severe weather, or safe for
high-pressure washdown.

Design priorities
-----------------

* Replace the exposed A1-class scanner with the planned **RPLIDAR S2 30 m
  (IP65)** while keeping the ROS ``/scan`` interface.
* Seal enclosure seams and cable penetrations without trapping heat.
* Add cable glands, grommets, drip loops, covers, and strain relief where needed.
* Shield exposed connectors from direct spray and alkaline dust.
* Keep service access practical instead of permanently sealing maintenance items.
* Validate cooling after enclosure changes around the Jetson and motor electronics.

Acceptance checks
-----------------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Check
     - Evidence
   * - Light rain / splash
     - Controlled testing and inspection show protected components and exposed
       connections are not compromised and the system remains functional.
   * - Alkaline dust
     - Critical openings and connectors are shielded from direct wind-carried
       alkaline dust during the supervised test condition.
   * - LiDAR
     - The installed IP-rated scanner publishes usable ``/scan`` data after
       its serial/udev configuration is updated.
   * - Thermal behavior
     - Weather-protection changes do not create unsafe compute or motor-control temperatures.
   * - Serviceability
     - Routine maintenance can be performed without destroying the intended seals.
