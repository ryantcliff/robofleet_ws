Hardware Commissioning
======================

Commission one subsystem at a time before running autonomous follow mode.


Physical inventory and electrical hold (2026-10-28)
---------------------------------------------------

See :doc:`../project/hardware_inventory` for the parts we have identified,
:doc:`../project/hardware_photo_findings` for physical inspection and
:doc:`../project/hardware_audit_checklist` for verification steps.

.. warning::

   The observed ODESC V4.2 motor controllers show 24 V markings while the
   existing seven-series motor battery can reach 29.4 V fully charged.
   Confirm the actual safe input rating of all four controllers before
   reconnecting motor power. The currently observed scanner is RPLIDAR
   A1M8; RPLIDAR S2 remains a planned upgrade. The required BNO085 is
   not confirmed installed.

Current hardware assignment
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 52 24

   * - Subsystem
     - Current / intended device
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
     - BNO085-class IMU; Adafruit #4754 is the preferred board
     - :planned:`Required upgrade`
   * - LiDAR
     - RPLIDAR S2 30 m, IP65
     - :planned:`Planned replacement for A1-class scanner`
   * - Short-range safety
     - Existing ultrasonic sensor array / microcontroller
     - :inherited:`Retain`
   * - Motors
     - ODrive-controlled four-BLDC drivetrain
     - :inherited:`Inherited`

BNO085 wiring target
--------------------

::

   Jetson pin 1  (3.3 V) --> BNO085 VIN
   Jetson pin 6  (GND)   --> BNO085 GND
   Jetson pin 27 (SDA)   --> BNO085 SDA
   Jetson pin 28 (SCL)   --> BNO085 SCL

The current configuration expects ``/dev/i2c-1``, address ``0x4A``, and 50 Hz
output. Verify the actual Linux bus and device address:

.. code-block:: bash

   i2cdetect -l
   sudo i2cdetect -y -r 1

RPLIDAR replacement
-------------------

The requirements document identifies the **RPLIDAR S2 30 m (IP65)** as the
planned weather-resistant replacement for the inherited A1-class scanner.
After installation:

* confirm the USB adapter's actual vendor/product ID;
* update the udev rule if the new adapter does not match the inherited CP2102 rule;
* update the required serial baud rate for the purchased S2 model;
* verify ``/scan``, timestamps, frame ID, and Nav2 obstacle behavior before field testing.

Stable device names
-------------------

The repository includes udev rules for stable paths such as
``/dev/ublox_gps`` and ``/dev/rplidar_usb``. Recheck USB vendor/product IDs
whenever a sensor or USB adapter is replaced.
