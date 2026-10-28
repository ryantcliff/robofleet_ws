Hardware Commissioning
======================

Bring up one subsystem at a time, and get each one working before you try
autonomous follow mode.

Inventory and the voltage problem
---------------------------------

Our parts list is in :doc:`../project/hardware_inventory`, the checks we still
want to do are in :doc:`../project/hardware_audit_checklist`, and the motor
power details are in :doc:`../project/electrical_review`.

.. warning::

   The motor controllers (ODESC V4.2) are marked 24 V, and our 7S motor
   battery charges to 29.4 V. The power transistors on them are rated 30 V
   absolute maximum, so there is almost no room above a full pack. Read
   :doc:`../project/electrical_review` before you power the motors.

   The LiDAR on the robot is an RPLIDAR A1M8. The S2 is only planned. We have
   not installed the BNO085.

What is on the robot
--------------------

.. list-table::
   :header-rows: 1
   :widths: 24 52 24

   * - Subsystem
     - Device
     - Status
   * - Compute
     - NVIDIA Jetson Orin Nano
     - :inherited:`Inherited / retain`
   * - FleetBot GNSS
     - u-blox ZED-F9P (SparkFun GPS-RTK2) over USB
     - :ready:`Integrated`
   * - RoboBeacon GNSS
     - u-blox NEO-M8P-2 -> HC-12 transmitter
     - :ready:`Configured / software path present`
   * - IMU
     - BNO085-class IMU; Adafruit #4754 is the board we would pick
     - :planned:`Required upgrade`
   * - LiDAR
     - RPLIDAR S2 30 m, IP65
     - :planned:`Planned replacement for the A1`
   * - Short-range safety
     - Ultrasonic sensors on an Arduino Nano
     - :inherited:`Retain`
   * - Motors
     - Four BLDC motors on ODrive-type controllers
     - :inherited:`Inherited`

BNO085 wiring
-------------

::

   Jetson pin 1  (3.3 V) --> BNO085 VIN
   Jetson pin 6  (GND)   --> BNO085 GND
   Jetson pin 27 (SDA)   --> BNO085 SDA
   Jetson pin 28 (SCL)   --> BNO085 SCL

The config expects bus ``/dev/i2c-1``, address ``0x4A``, and 50 Hz output.
Check the real bus and address:

.. code-block:: bash

   i2cdetect -l
   sudo i2cdetect -y -r 1

Swapping in the RPLIDAR S2
--------------------------

Our requirements name the **RPLIDAR S2 30 m (IP65)** as the weatherproof
replacement for the A1. After it is installed:

* check the USB adapter's real vendor and product ID;
* change the udev rule if the new adapter does not match the old CP2102 rule;
* set the serial baud rate that the S2 needs;
* confirm ``/scan``, its timestamps, the frame ID and Nav2's obstacle behavior
  before any field test.

Stable device names
-------------------

The repo has udev rules so the devices keep fixed paths, like ``/dev/ublox_gps``
and ``/dev/rplidar_usb``. If you change a sensor or USB adapter, check its
vendor and product ID again.
