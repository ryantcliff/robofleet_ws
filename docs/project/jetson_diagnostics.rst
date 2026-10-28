Jetson diagnostics - October 28, 2026
=====================================

On October 28 we went through the FleetBot's Jetson Orin Nano and the drive
software that runs on it. We started with read-only checks. Then we ran the
drive controller by itself (without the e-stop node, so it could not arm) and read
each motor controller's bus voltage over USB. We never sent a motor command.

For each item we say whether we **confirmed** it, **saw** it (and are inferring
the cause), or **have not checked** it.

The Jetson
----------

* Confirmed: Jetson Orin Nano Developer Kit, Ubuntu 22.04.5, kernel
  ``5.15.148-tegra``, ROS 2 Humble, 64 GB SD card about 64% full.
* Saw: no battery-backed clock. The time jumps forward while it boots, so
  early boot log timestamps are wrong.
* Saw: the filesystem recovered from an unclean shutdown at boot. We found no
  storage errors in the logs we had. We do not know what caused the shutdown.

Parts vs. our inventory
-----------------------

.. list-table::
   :header-rows: 1

   * - Part
     - What we found
   * - ZED-F9P GPS
     - Present as ``/dev/ublox_gps``. We listened without writing to it and saw
       empty ``GNGGA`` sentences (quality 0, no satellites), so no fix. RTK
       is not tested.
   * - RPLIDAR A1M8
     - Its USB-UART adapter is there as ``/dev/rplidar_usb``. We have not taken a
       scan.
   * - Ultrasonic Arduino Nano
     - Present as ``/dev/arduino_nano``.
   * - Meshtastic T-Beam
     - Present as ``/dev/meshtastic``.
   * - Four ODESC controllers
     - Not on USB until we connected the motor battery, then all four showed up.
   * - IMU (MPU-6050 / BNO085)
     - Have not checked. We have not probed I2C.
   * - HC-12 radio
     - ``/dev/ttyTHS1`` exists. We have not checked the module's wiring.

The drive software
------------------

What we found:

* ``roboflock-drive.service`` (from ``src/bring_up/systemd``) was installed and
  enabled, so the joystick drive stack started every time the Jetson booted.
* With the old code, ``diff_drive_controller`` waited for the ODESCs with no
  timeout. When we connected the motor battery it connected to all four
  controllers by itself, cleared their errors, and wrote velocity settings.
  Pressing **Options** on the PS4 controller then released the software e-stop
  and put all four axes into closed-loop control. **Cross** put them back to
  idle.
* The ultrasonic publisher did not recover when the Arduino showed up after the
  node started. ``ultrasonic_estop`` kept saying it was not guarding anything.
* ``ultrasonic_estop`` ignored a sensor that had gone quiet, so a failed or disconnected Arduino
  meant no obstacle backup at all.
* ``diff_drive_controller`` printed two lines for every velocity command, which
  was filling the journal on the SD card.

What we did:

* ``diff_drive_controller`` now waits 2 s per controller and keeps retrying the
  missing ones. When we ran it on the robot, all four connected in under a
  second and it stayed idle with no e-stop node running. Unit tests cover a
  controller missing at startup.
* ``ultrasonic_publisher`` keeps retrying every second until the Arduino
  appears. We have not yet tested this by unplugging and replugging the Arduino.
* ``ultrasonic_estop`` now blocks forward motion when any sensor goes quiet.
  Reverse and turning still work. We tested it with the real Arduino: with no
  sensor data a 0.3 forward command came out as 0, with fresh clear readings it
  passed through, and with a close reading it was blocked.
* The per-command log lines are now debug level.
* We turned the service off, and its unit file now points at this repo's
  workspace.

Still not fixed
---------------

* One press of Options arms the motors, and a stop only idles them, so the
  wheels coast. We found no physical power cut.
* The ultrasonic check blocks forward motion only.
* The motor voltage margin: the pack charges to 29.4 V and the power MOSFETs are
  rated 30 V absolute maximum. See :doc:`electrical_review`.

Not checked yet
---------------

Anything on the electrical side we have not measured with a meter, the IMU, a
real GPS fix, a LiDAR scan, and the unplug/replug behavior of the Arduino and
the motor controllers on the robot.
