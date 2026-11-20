FleetBot hardware commissioning checklist
==========================================

This checklist combines inherited instructions with currently known safety
limitations. **Do not power the drive system simply to run the checklist.**
The motor-battery/controller rating discrepancy and absence of a physical
power cutoff require a separate risk review. See
:doc:`../project/electrical_review` and :doc:`../project/hardware_audit_checklist`.

Record every result with the test date, observer, measured value,
instrument/command, and whether it passed or remains unverified.

1. Identify hardware without actuation
--------------------------------------

* Compare the installed Jetson, GPS, IMU, lidar, Arduino, HC-12, battery,
  fuses and four ODESC controllers with :doc:`../project/hardware_inventory`.
* Check cables, fuse markings, battery label, polarity and mounting
  **without disturbing energized connectors**.
* Check whether ``roboflock-drive.service`` is installed/enabled; it can
  start the joystick/motor software automatically. Do not activate it
  during inspection.
* Check serial-device enumeration with ``lsusb``, ``ls -l /dev/serial/by-id``
  and ``dmesg``. Prefer non-invasive observations.

2. Serial device names and permissions
--------------------------------------

The inherited rule file is
``src/bring_up/udev/99-roboflock.rules``. It maps device IDs to
``/dev/ublox_gps``, ``/dev/rplidar_usb``, ``/dev/meshtastic`` and
``/dev/arduino_nano``. Match USB identifiers against the real
hardware **before** installing rules; broad 0666 permissions in the
inherited file deserve a separate security review.

When the rules are verified and you intentionally elect to install them:

.. code-block:: bash

   sudo usermod -aG dialout roboflock
   sudo cp src/bring_up/udev/99-roboflock.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules
   sudo udevadm trigger

Group changes usually require a new login. Check the actual Jetson username
and paths first. This is a **configuration-changing** procedure, not a
read-only diagnostic step.

3. Sensors and localization
---------------------------

* Check the ZED-F9P's USB data cable (not charge-only), dual-band antenna,
  fix type, covariance and correction source.
* Verify the inherited GPS antenna transform, historically noted as about
  0.16 m forward and 0.63 m above ground, by physical measurement and URDF.
* Install and mount a BNO085-class IMU before depending on GPS heading.
  Check I2C bus/address, orientation, magnetic declination and ENU yaw.
* Verify real lidar scan timestamps, ``/scan`` frame and TF.
* Check that Arduino ultrasonic data resumes after unplug/replug, and that
  a missing sensor fails closed as intended.
* Record five minutes of stationary ``/odometry/global`` to measure drift
  **only after** localization has a valid heading and GPS fix.

4. RoboBeacon and optional home station
---------------------------------------

* Verify NEO-M8P GGA output and received ``/gps/beacon/fix`` messages.
* Check radio range, missing-data timeout and GPS stand-off accuracy.
* If testing the optional Meshtastic path, verify the ROBT/HOME/TOM radio
  settings, command delivery and outdoor HOME position.
* Never commit private Meshtastic channel keys or configuration secrets.

5. Motor and field-test gate
----------------------------

**Do not run powered motor tests until the electrical risk review and an
effective stop procedure have been addressed.** At present there is no
verified physical cutoff, and the inspected MOSFET voltage limit is close
to a fully charged pack.

When a responsible team review authorizes a controlled test, document
PS4 Cross/Options behavior, lost-joystick watchdog, stale command
handling, braking and clear wheel separation from the ground. Test with
a spotter and safe access to a physical power disconnect.

Only after sensor calibration, software checks and power review should
the team attempt a low-speed open-field demo. Keep the walker well ahead
(historic plan: at least 10 m initially), maintain operator control,
and log the actual 1.5–3.0 m stand-off performance.

See :doc:`simulation` for hardware-free test commands and
:doc:`../project/requirements` for the formal acceptance criteria.
