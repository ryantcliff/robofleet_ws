Obstacle Detection
==================

The robot uses a 360-degree 2-D RPLIDAR as its main obstacle sensor. Ultrasonic
sensors on the front are a short-range backup.

Ultrasonic backup
-----------------

Three ultrasonic sensors (left, center, right) on an Arduino Nano publish range
readings at 20 Hz. ``ultrasonic_estop`` sits between ``twist_mux`` and the motor
controller. It blocks forward motion when any sensor reads closer than 0.5 m on
two consecutive readings (about 50 ms), which filters out a single bad echo. One
reading at or beyond 0.5 m, or no echo, clears the block. Reversing and turning
stay allowed so the operator can back away.

A sensor with no reading for 1.0 s counts as silent. With the default
``fail_closed:=true``, a silent sensor also blocks forward motion. This covers an
unplugged or crashed Arduino and the case where it enumerates after the node
starts. Previously the node ignored silent sensors, so a missing Arduino left
the robot with no backup and only a log warning. Setting ``fail_closed:=false``
restores that behavior.

This is a last-resort backstop for obstacles the LiDAR cannot see, such as
objects below its scan plane. It does not replace the LiDAR.

LiDAR upgrade
-------------

We plan to replace the exposed A1 with an IP-rated RPLIDAR S2, so dust and rain
are handled at the sensor itself.

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Item
     - Inherited
     - What we are doing
   * - LiDAR
     - A1-class serial RPLIDAR
     - IP65 S2-class RPLIDAR
   * - ROS topic
     - ``/scan``
     - Keep ``/scan`` so the software barely changes
   * - Serial speed
     - 115200 baud
     - Set the baud rate the S2 needs
   * - Backup sensors
     - Ultrasonic
     - Keep and test them

.. important:: An IP65 LiDAR does not make the robot IP65

   The cable exit, the USB/serial adapter, the mount and the electronics
   enclosure still need sealing and strain relief.
