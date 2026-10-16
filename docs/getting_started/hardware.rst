Hardware Commissioning
======================

Commission one subsystem at a time before running autonomous follow mode.

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
     - :inherited:`Inherited`
   * - Robot GNSS
     - u-blox ZED-F9P over USB
     - :ready:`Integrated`
   * - Beacon GNSS
     - u-blox NEO-M8P -> HC-12 transmitter
     - :ready:`Software path present`
   * - IMU
     - Adafruit BNO085 on I2C
     - :planned:`Upgrade`
   * - LiDAR
     - RPLIDAR; IP-rated S2-class replacement planned
     - :planned:`Upgrade`
   * - Motors
     - ODrive-controlled BLDC drivetrain
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

Stable device names
-------------------

The repository includes udev rules for stable paths such as
``/dev/ublox_gps`` and ``/dev/rplidar_usb``. Recheck USB vendor/product IDs
whenever a sensor or USB adapter is replaced.
