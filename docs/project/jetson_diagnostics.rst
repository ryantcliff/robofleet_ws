Jetson read-only diagnostics — October 28, 2026
================================================

Findings from a read-only diagnostic of the FleetBot's Jetson Orin Nano and a
review of the on-robot drive stack. No motor commands were issued. Each item
is labelled **Confirmed** (observed directly), **Observed** (seen, cause
inferred) or **Not verified**.

Platform
--------

* Confirmed: Jetson Orin Nano Developer Kit, Ubuntu 22.04.5, kernel
  ``5.15.148-tegra``, ROS 2 Humble, root filesystem on a 64 GB SD card (about
  64% used).
* Observed: the system clock has no battery-backed RTC and steps forward during
  boot, so early-boot log timestamps are unreliable.
* Observed: the filesystem recovered from an unclean shutdown at boot. No
  storage I/O errors were found in the logs that were retained. The cause of
  the unclean shutdown is not verified.

Peripherals compared with the inventory
---------------------------------------

.. list-table::
   :header-rows: 1

   * - Item
     - Result
   * - ZED-F9P GNSS receiver
     - Confirmed present as ``/dev/ublox_gps``. A passive listen showed empty
       ``GNGGA`` sentences (quality 0, no satellites), so no fix at the time of
       the check; RTK is not verified.
   * - RPLIDAR A1M8
     - Confirmed: USB-UART adapter present as ``/dev/rplidar_usb``. No scan was
       taken.
   * - Ultrasonic Arduino Nano
     - Confirmed present as ``/dev/arduino_nano``.
   * - Meshtastic T-Beam
     - Confirmed present as ``/dev/meshtastic``.
   * - Four ODESC controllers
     - Appeared on USB when the motor battery was connected; absent before.
   * - IMU (MPU-6050 / BNO085)
     - Not verified. I2C was not probed.
   * - HC-12 radio
     - ``/dev/ttyTHS1`` exists; module wiring not verified.

Drive stack behaviour
---------------------

* Confirmed: ``roboflock-drive.service`` (from ``src/bring_up/systemd``) was
  installed and enabled on the robot. It started the joystick drive stack at
  every boot.
* Confirmed: with the previous code, ``diff_drive_controller`` waited for the
  ODESCs with no timeout. When the motor battery was connected it connected to
  all four controllers on its own, cleared their errors and wrote velocity
  settings. A single press of **Options** on the controller then released the
  software e-stop and moved all four axes to closed-loop control. Pressing
  **Cross** idled them again.
* Confirmed: the ultrasonic publisher did not recover when the Arduino
  enumerated after the node started, so ``ultrasonic_estop`` reported "not
  guarding" indefinitely.
* Both startup problems are addressed by the *don't hang at startup waiting for
  hardware* change. With it, all four ODESCs connected in under one second and
  the node stayed idle with no e-stop publisher running. Unit tests cover a
  controller missing at startup; the Arduino retry has not been run on the
  robot.

Safety limitations (unchanged)
------------------------------

* The software e-stop is released by one button press. Stop sets the axes to
  idle (the wheels coast); no hardware power cut was documented or observed.
* The ultrasonic check ignores sensors with no recent reading, and only blocks
  forward motion.
* Motor-bus voltage margin remains an open hardware question: the motor pack
  charges to 29.4 V and a photographed power MOSFET is rated 30 V absolute
  maximum. Bus voltage, transients, fuse ratings and braking-resistor mounting
  have not been measured. See :doc:`hardware_photo_findings`.

Not checked
-----------

Electrical state, stored ODESC configuration, IMU hardware, a GPS fix, LiDAR
scans, and whether a hardware stop exists.
