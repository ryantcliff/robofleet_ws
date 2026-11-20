Weatherproofing
===============

Weather protection is one of our formal requirements. We need to protect the
critical parts and exposed connections during **supervised outdoor use in light
rain, incidental splashes, and wind carrying alkaline dust**.

We are not claiming the whole FleetBot has an IP rating, can be submerged, can
sit out unattended in bad weather, or can be pressure washed.

What we plan to do
------------------

* Replace the exposed A1 scanner with the **RPLIDAR S2 30 m (IP65)** and keep
  the ROS ``/scan`` interface the same.
* Seal enclosure seams and cable entries without trapping heat.
* Add cable glands, grommets, drip loops, covers and strain relief where
  needed.
* Shield exposed connectors from direct spray and alkaline dust.
* Keep service access practical, and do not permanently seal things we have to
  maintain.
* Recheck cooling around the Jetson and the motor electronics after any
  enclosure change.

How we will check it
--------------------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Check
     - What we need to see
   * - Light rain / splash
     - In a controlled test, the protected parts and exposed connections are
       fine and the robot still works.
   * - Alkaline dust
     - Critical openings and connectors are shielded from wind-blown dust during
       the supervised test.
   * - LiDAR
     - The IP-rated scanner publishes usable ``/scan`` data once its serial and
       udev settings are updated.
   * - Heat
     - Our weather protection does not push the compute or motor electronics to
       unsafe temperatures.
   * - Serviceability
     - Routine maintenance can be done without damaging the seals.
