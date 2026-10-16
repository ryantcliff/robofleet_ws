Weatherproofing
===============

Weatherproofing is a formal current-year requirement. The objective is not to
claim full waterproofing, but to make the robot substantially more tolerant of
dust, rain, wet ground, and outdoor operation while keeping service access
practical.

Design priorities
-----------------

* Use IP-rated sensors where practical, beginning with the 360-degree LiDAR.
* Seal enclosure seams and cable penetrations without trapping heat.
* Add grommets, glands, drip loops, and strain relief to external wiring.
* Keep connectors accessible for maintenance while shielding them from direct spray.
* Separate likely water paths from high-current power electronics.
* Validate cooling after enclosure changes around the Jetson and ODrives.

Acceptance checks
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Check
     - Evidence
   * - Dust ingress
     - No exposed openings that lead directly to compute or motor-control electronics.
   * - Rain / splash resistance
     - External sensor housings and cable entries remain protected during controlled spray testing.
   * - Thermal behavior
     - Jetson and motor electronics remain within safe operating temperature after sealing.
   * - Serviceability
     - Common maintenance items remain removable without destroying seals.
