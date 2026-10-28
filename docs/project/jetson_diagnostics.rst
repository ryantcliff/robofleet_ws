Jetson diagnostics — October 28, 2026
=====================================

On October 28, 2026 we ran a diagnostic on the FleetBot's Jetson Orin Nano and
reviewed the drive stack that runs on it. We began with read-only checks, then
ran the drive controller on its own (without the e-stop node, so it could not
arm) and read each motor controller's bus voltage over USB. We sent no motor
commands. Each item is labelled **Confirmed** (we observed it directly),
**Observed** (we saw it and have inferred the cause) or **Not verified**.

Platform
--------

* Confirmed: Jetson Orin Nano Developer Kit, Ubuntu 22.04.5, kernel
  ``5.15.148-tegra``, ROS 2 Humble, root filesystem on a 64 GB SD card (about
  64% used).
* Observed: the system clock has no battery-backed RTC and steps forward during
  boot, so early-boot log timestamps are unreliable.
* Observed: the filesystem recovered from an unclean shutdown at boot. We found
  no storage I/O errors in the logs that were retained. We have not verified
  the cause of the unclean shutdown.

Peripherals compared with the inventory
---------------------------------------

.. list-table::
   :header-rows: 1

   * - Item
     - Result
   * - ZED-F9P GNSS receiver
     - Confirmed present as ``/dev/ublox_gps``. A passive listen showed empty
       ``GNGGA`` sentences (quality 0, no satellites), so there was no fix at
       the time of the check. RTK is not verified.
   * - RPLIDAR A1M8
     - Confirmed: USB-UART adapter present as ``/dev/rplidar_usb``. We have not
       yet taken a scan.
   * - Ultrasonic Arduino Nano
     - Confirmed present as ``/dev/arduino_nano``.
   * - Meshtastic T-Beam
     - Confirmed present as ``/dev/meshtastic``.
   * - Four ODESC controllers
     - Absent from USB until we connected the motor battery, then all four
       appeared.
   * - IMU (MPU-6050 / BNO085)
     - Not verified. We have not probed I2C.
   * - HC-12 radio
     - ``/dev/ttyTHS1`` exists. We have not verified the module wiring.

Drive stack behaviour
---------------------

* Confirmed: ``roboflock-drive.service`` (from ``src/bring_up/systemd``) was
  installed and enabled on the robot and started the joystick drive stack at
  every boot. We have since disabled it, and its unit now points at this
  repository's workspace.
* Confirmed: before our fix, ``diff_drive_controller`` waited for the ODESCs
  with no timeout. When we connected the motor battery it connected to all four
  controllers on its own, cleared their errors and wrote velocity settings. A
  single press of **Options** on the controller then released the software
  e-stop and moved all four axes to closed-loop control, and **Cross** idled
  them again.
* Confirmed: the ultrasonic publisher did not recover when the Arduino
  enumerated after the node started, so ``ultrasonic_estop`` reported "not
  guarding" indefinitely.
* We fixed both startup problems. With the fix, all four ODESCs connected in
  under one second and the node stayed idle with no e-stop publisher running.
  Unit tests cover a controller missing at startup. We have not yet tested the
  Arduino retry by unplugging and replugging it on the robot.
* ``ultrasonic_estop`` now blocks forward motion when any ultrasonic sensor has
  gone quiet, instead of ignoring it. Reversing and turning stay allowed.
* ``diff_drive_controller`` no longer prints every velocity command to the log,
  which was filling the journal on the SD card.

Safety limitations that remain
------------------------------

* The software e-stop is released by one button press. Stop sets the axes to
  idle (the wheels coast). We have not documented or found a hardware power
  cut.
* The ultrasonic check blocks forward motion only.
* The motor-bus voltage margin is still an open hardware question: the motor
  pack charges to 29.4 V and a photographed power MOSFET is rated 30 V absolute
  maximum. We have not measured bus voltage, transients, fuse ratings or
  braking-resistor mounting. See :doc:`electrical_review` and
  :doc:`hardware_photo_findings`.

Not yet checked
---------------

Electrical state, stored ODESC configuration beyond what :doc:`electrical_review`
records, IMU hardware, a GPS fix, LiDAR scans, and whether a hardware stop
exists.
