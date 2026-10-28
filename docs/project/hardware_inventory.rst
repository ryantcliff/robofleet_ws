FleetBot hardware inventory — physical audit (2026-10-28)
========================================================

This is an inventory of physically identified hardware, not a validated
electrical schematic or proof of operation. RoboFleet continues inherited
RoboFlock equipment. The required 2026–2027 delivery is one FleetBot.

.. warning::

   Do not energize the motor drivetrain until all four motor-controller
   voltage ratings have been positively identified. The photographed ODESC
   V4.2 boards have visible 24 V QC markings. The HOT PAXX 7S4P pack has a
   labeled 29.4 V full-charge voltage. A controller rated only to 24 V
   cannot safely be assumed compatible with that pack. Capacitors marked
   63 V do not establish the safe input voltage of the entire board.

Team-observed hardware
----------------------

.. list-table::
   :header-rows: 1
   :widths: 10 8 58 24

   * - ID
     - Qty
     - Identified hardware
     - Verification status
   * - RF-001
     - 3
     - LILYGO T-Beam AXP2101 V1.2, 868/915 MHz LoRa marking,
       u-blox NEO-6M (HOME / TOM / ROBOT)
     - Observed; radio chip/config unverified
   * - RF-002
     - 4
     - Four identical ODESC V4.2 motor controllers; FL, FR, RL, RR
     - Identical hardware confirmed by team; unsafe 7S voltage margin
   * - RF-003
     - 1
     - Zeee 6000 mAh 3S 11.1 V 66.6 Wh LiPo (Jetson battery)
     - Observed; output/load untested
   * - RF-004
     - 1
     - HOT PAXX 7S4P 25.2 V 20 Ah 504 Wh lithium-ion motor pack;
       29.4 V charging, 40 A continuous and 60 A peak BMS labels
     - Observed; controller compatibility unresolved
   * - RF-005
     - 1
     - Sabrent HB-UMLS USB 2.0 four-port hub
     - Observed; Arduino and dev peripherals
   * - RF-006
     - 1
     - Unmarked USB-C upstream / four USB-A downstream hub
     - Observed; four motor-controller USB links
   * - RF-007
     - 1
     - SparkFun GPS-RTK2 with u-blox ZED-F9P-02B-00
     - Observed; RTK status untested
   * - RF-008
     - 1
     - LM2596 adjustable DC-DC buck board
     - Observed; voltage and load capacity untested
   * - RF-009
     - 2
     - Unmarked fuse/distribution blocks (one Jetson, four ODESC branches)
     - Observed; fuse values unknown
   * - RF-010
     - 4
     - STEPPERONLINE M82B200-24P-30S/G82-30S1,
       24 V 200 W geared BLDC motors
     - Observed
   * - RF-011
     - 4
     - Pneumatic tires marked 4.10/3.50-4 on metal rims,
       roughly 10-inch outside diameter
     - Photo-confirmed; tire pressure/hub unknown
   * - RF-012
     - 1
     - Arduino Nano, ATmega328P-marked
     - Observed; pin assignments unverified
   * - RF-013
     - 3
     - HC-SR04 ultrasonic sensors per team inventory
     - Observed; exposed sensor-board model confirmation pending
   * - RF-014
     - 1
     - RPLIDAR A1M8 (STC-A0317-R03 marking)
     - Observed; existing LiDAR, not S2
   * - RF-015
     - 1
     - u-blox ANN-MB2-00-00 active multiband GNSS antenna
     - Observed; actual cable pairing unknown
   * - RF-016
     - 1
     - SparkFun u-blox NEO-M8P-2-12 receiver (RoboBeacon)
     - Observed; breakout revision unknown
   * - RF-017
     - 1
     - u-blox ANN-MB-00-00 L1/L2 active GNSS antenna
     - Observed; actual cable pairing unknown
   * - RF-018
     - 2
     - HC-12 433 MHz serial radio modules
     - Observed; RoboBeacon TX / FleetBot RX
   * - RF-019
     - 1
     - Surface Go 2 tablet, Pentium 4425Y, 4 GB RAM,
       Windows 10 Pro 22H2
     - Available; future home-base role unconfirmed
   * - RF-020
     - 1
     - NVIDIA Jetson Orin Nano Developer Kit
     - Observed; inherited onboard compute

Electrical architecture: observed versus unverified
---------------------------------------------------

* Zeee 3S battery -> fused LM2596 buck board -> Jetson DC input is
  described by team inspection. An LM2596 is a step-down converter, not a
  boost converter. Measure actual output voltage and regulation under load.
* HOT PAXX 7S motor battery -> four fused ODESC supplies is described
  by team inspection. Record exact fuse values, wire gauge, disconnects,
  controller bus ratings and transient/regen protection before energizing.
* Team confirms all four ODESC boards are identical. A close-up of RL identifies
  JMTG3002B MOSFETs with 30 V absolute-maximum drain-source rating, only 0.6 V
  above the 7S battery full-charge voltage. Avoid direct 7S operation;
  investigate a compatible motor power architecture.
* Four orange aluminum-cased resistors are marked 50W 2RJ, consistent
  with 2 ohm / 50 W braking resistors. Their wiring, firmware configuration,
  electrical pulse rating and heat sinking remain to be checked.
* Four USB-connected ODESC devices share one unidentified hub. Verify
  the hub power arrangement, enumeration and disconnect behavior.
* ZED-F9P offers RTK capability but actual fix/correction quality is
  unmeasured; do not assume centimeter-grade tracking.
* HOME/TOM/ROBOT T-Beams are optional communications equipment under
  the present contractual scope, not a finished home-base assembly.

Mechanical and weather observations
-----------------------------------

Photos show aluminum T-slot extrusions, custom-looking printed motor supports,
custom wheel/shaft couplings, a partly exposed sensor bar, and an open-topped
electronics container. Four pneumatic wheels have metal rims and valve stems.
The shaft retention, hub material, independent wheel bearings, wheelbase,
track, loaded radius, and mounting hardware remain to be measured.

Visible exposed electronics and connections do not establish weather
protection under requirement R-6. No whole-FleetBot IP rating is claimed.

Required/planned parts not confirmed installed
-----------------------------------------------

* BNO085-class absolute-heading IMU — required upgrade.
* RPLIDAR S2 30 m weather-resistant scanner — planned upgrade.
* Verified physical e-stop, disconnect, fused/appropriate motor harness,
  weather-protected connectors and sealed electronics enclosure —
  installation/ratings unverified.

Cross-references
----------------

See the hardware photo findings and audit checklist in this section for the
photo-to-controller mapping and the open verification tasks. Formal work
scope is in the requirements page.

External references (not proof of the particular installed variant):

* NVIDIA: https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/latest/hardware_layout.html
* LM2596: https://www.ti.com/product/LM2596
* Sabrent HB-UMLS: https://sabrent.com/products/hb-umls
* STEPPERONLINE motor: https://www.stepperonline.co.uk/24v-200w-100rpm-geared-brushless-dc-motor-15-00nm-2124-17oz-in-30-1-planetary-gearbox-m82b200-24p-30s-g82-30s1.html
* u-blox ZED-F9P: https://content.u-blox.com/sites/default/files/documents/ZED-F9P-02B_DataSheet_UBX-21023276.pdf

For privacy, this public page excludes individual serial numbers, Windows
device identifiers, private radio identifiers, encryption keys and raw
inspection photographs.
