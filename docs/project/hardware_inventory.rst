FleetBot hardware inventory — physical audit (2026-10-28)
=========================================================

This is a list of the hardware we have physically found and looked at. It is not a
wiring diagram, and being on this list does not mean a part works. RoboFleet
reuses RoboFlock's equipment, and what we owe this year is one FleetBot.

.. warning::

   The motor power is the biggest risk we know about. All four ODESC
   controllers are the same, and the one we opened (RL) has JMTG3002B power
   MOSFETs rated 30 V absolute maximum. Our 7S pack charges to 29.4 V, which
   leaves 0.6 V before switching and braking spikes. We are still using the
   pack and controllers. Read :doc:`electrical_review` for what we measured and
   what we have done about it.

What we have identified
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 10 8 56 26

   * - ID
     - Qty
     - What it is
     - Where we stand
   * - RF-001
     - 3
     - LILYGO T-Beam AXP2101 V1.2 (868/915 MHz LoRa marking, u-blox
       NEO-6M). Named HOME, TOM and ROBOT.
     - Inspected. Radio chip and config not checked.
   * - RF-002
     - 4
     - ODESC V4.2 motor controllers at FL, FR, RL and RR. All four are
       identical. Firmware 0.5.6 on hardware 3.6.24.
     - Seen and read over USB. The voltage margin is a problem; see the
       electrical review.
   * - RF-003
     - 1
     - Zeee 6000 mAh 3S 11.1 V 66.6 Wh LiPo (Jetson battery).
     - Inspected. Not tested under load.
   * - RF-004
     - 1
     - HOT PAXX 7S4P lithium-ion motor pack, 25.2 V nominal, 20 Ah, 504
       Wh, EVE 21700 50E cells. BMS: ChangFa 40 A continuous, 60 A peak,
       19 V minimum. XT90 discharge port, XT60 charge port (29.4 V, up to
       5 A).
     - Label read. Whether it suits the controllers is the open problem.
   * - RF-005
     - 1
     - Sabrent HB-UMLS USB 2.0 four-port hub.
     - Inspected. Arduino and dev peripherals.
   * - RF-006
     - 1
     - Unmarked hub, USB-C upstream and four USB-A downstream.
     - Inspected. The four motor-controller USB links.
   * - RF-007
     - 1
     - SparkFun GPS-RTK2 with u-blox ZED-F9P-02B-00.
     - Inspected. RTK not tested. No fix when we listened (quality 0, no satellites).
   * - RF-008
     - 1
     - LM2596 adjustable DC-DC buck board.
     - Inspected. Output voltage and load not tested.
   * - RF-009
     - 2
     - Two fuse blocks. Motor block: four yellow 20 A fuses, one per
       controller. Jetson block: one 5 A fuse.
     - Seen, values read. There is no main fuse.
   * - RF-010
     - 4
     - STEPPERONLINE M82B200-24P-30S/G82-30S1, 24 V 200 W geared BLDC
       motors.
     - Inspected.
   * - RF-011
     - 4
     - Pneumatic tires marked 4.10/3.50-4 on metal rims, about 10 in
       outside diameter.
     - Confirmed by inspection. Tire pressure and hub details unknown.
   * - RF-012
     - 1
     - Arduino Nano (ATmega328P).
     - Inspected. Pin assignments not checked.
   * - RF-013
     - 3
     - HC-SR04 ultrasonic sensors, per our inventory.
     - Inspected. Sensor-board model not confirmed.
   * - RF-014
     - 1
     - RPLIDAR A1M8 (marked STC-A0317-R03).
     - Inspected. This is the LiDAR we have, not the S2.
   * - RF-015
     - 1
     - u-blox ANN-MB2-00-00 active multiband GNSS antenna.
     - Inspected. Which receiver it is cabled to is not confirmed.
   * - RF-016
     - 1
     - SparkFun u-blox NEO-M8P-2-12 receiver (the RoboBeacon).
     - Inspected. Breakout revision unknown.
   * - RF-017
     - 1
     - u-blox ANN-MB-00-00 L1/L2 active GNSS antenna.
     - Inspected. Which receiver it is cabled to is not confirmed.
   * - RF-018
     - 2
     - HC-12 433 MHz serial radios.
     - Inspected. One transmits for the RoboBeacon, one receives on the
       FleetBot.
   * - RF-019
     - 1
     - Surface Go 2, Pentium 4425Y, 4 GB RAM, Windows 10 Pro 22H2.
     - In our possession. We have not decided if it is the home base.
   * - RF-020
     - 1
     - NVIDIA Jetson Orin Nano Developer Kit. Runs Ubuntu 22.04.5 (L4T
       R36.4.7) and reports itself as the "Super" dev kit.
     - Inspected. Inherited.

A driving demonstration we were told about
------------------------------------------

We were told that the inherited FleetBot was driven around for **more than 30
minutes** with everything connected, including the motor battery and all four
controllers. That is good evidence the drivetrain works for a sustained run, and
it was more than a bench spin test. It happened before our inspection, and
nobody recorded the battery charge, the bus voltage or spikes, the peak load,
braking, the terrain, the temperatures, or any logs.

We take that as a reason to keep the working design while we investigate. It
does not tell us the voltage margin is fine. We have not chosen a replacement
battery, controller or converter.

Electrical setup: what we know and what we do not
-------------------------------------------------

* **Jetson power.** The Zeee 3S battery feeds a fuse, then the LM2596 buck board,
  then the Jetson's DC input. The LM2596 only steps voltage down. We have not
  measured its output under load.
* **Motor power.** The HOT PAXX 7S pack feeds the motor fuse block, with one
  20 A fuse for each controller. The motor cable is 10 AWG, 200 C rated, red on
  positive and black on negative. There is no main fuse and no disconnect; the
  only way to cut motor power is to unplug the XT90.
* **Controllers.** All four are the same. Read over USB they report hardware
  3.6.24 and firmware 0.5.6. The firmware's overvoltage trip is set to 32 V,
  above the transistors' 30 V rating. The ODrive documentation says the default
  for this board is 26 V.
* **Braking resistors.** Four orange aluminum 50W 2RJ resistors, 2 ohm, connected
  and measured. The controllers are set to use them (2.0 ohm, enabled). We
  have not checked the resistors' pulse rating or heat sinking.
* **USB.** All four controllers share one unmarked hub. We have not checked how
  it is powered or how it behaves when something is unplugged.
* **GPS.** The ZED-F9P can do RTK, but we have not measured the real fix or
  correction quality, so we are not assuming centimeter-level tracking.
* **T-Beams.** HOME, TOM and ROBOT are optional radios this year. They are not a
  finished home base.

Mechanical and weather
----------------------

Our inspection showed aluminum T-slot extrusions, custom printed motor mounts, custom
wheel and shaft couplings, a partly exposed sensor bar and an open-topped
electronics tray. The tires are pneumatic with metal rims and valve stems. We
still need to measure the shaft retention, hub material, wheel bearings,
wheelbase, track width, loaded radius and mounting hardware.

Exposed electronics do not count as weather protection under requirement R-6.
We are not claiming an IP rating for the whole FleetBot.

Required or planned parts we have not installed
-----------------------------------------------

* BNO085-class absolute-heading IMU (required upgrade).
* RPLIDAR S2 30 m weatherproof scanner (planned upgrade).
* A physical e-stop or disconnect, a fused motor harness that is rated for the
  pack, weatherproof connectors and a sealed electronics enclosure.

Markings we can read
--------------------

On the controllers we can read: ODESC V4.2, 24 V QC stickers, 100 uF / 63 V
capacitors, USB-C ports, terminals labeled motor A/C/B and DC +/-, and
terminals labeled AUX +/-. The orange aluminum resistor housings say 50W 2RJ,
which fits a 2 ohm, 50 W part. None of these markings tell us the controller's
real input voltage limit, whether the resistors are wired correctly, or whether
they have enough heat sinking.

On the underside of the rear-left (RL) controller we read the marking
JMT G3002B on several power-stage parts. That is the JieJie Microelectronics
JMTG3002B N-channel MOSFET, with a 30 V absolute-maximum drain-source voltage.
We have only read the MOSFET markings on RL. The other three controllers are
identical to it, which we know from their matching hardware and firmware versions.

Where to look next
------------------

The open checks are in the audit checklist, the motor power details are in the
electrical review, and the formal scope is on the requirements page.

References (these describe the parts in general, not our exact units):

* JieJie JMTG3002B datasheet, version 1.4: https://e-nexty.dxp.nexty-ele.com/product_files/download?maker_code=JJM&product_part_number=JMTG3002B&product_file_id=5467845&product_id=6198730&lc_code=ja&search_log_id=4389931
* NVIDIA: https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/latest/hardware_layout.html
* LM2596: https://www.ti.com/product/LM2596
* Sabrent HB-UMLS: https://sabrent.com/products/hb-umls
* STEPPERONLINE motor: https://www.stepperonline.co.uk/24v-200w-100rpm-geared-brushless-dc-motor-15-00nm-2124-17oz-in-30-1-planetary-gearbox-m82b200-24p-30s-g82-30s1.html
* u-blox ZED-F9P: https://content.u-blox.com/sites/default/files/documents/ZED-F9P-02B_DataSheet_UBX-21023276.pdf
