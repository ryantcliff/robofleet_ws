Obstacle Detection
==================

The inherited platform uses a 360-degree 2-D RPLIDAR for primary obstacle
perception and ultrasonic sensing as a short-range fail-safe.

Current-year environmental upgrade
----------------------------------

We plan to replace the exposed A1-class LiDAR with an IP-rated
RPLIDAR S2-class scanner so dust and rain are addressed at the sensor enclosure
level.

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Item
     - Inherited
     - 2026–2027 direction
   * - LiDAR
     - A1-class serial RPLIDAR
     - IP65 S2-class RPLIDAR
   * - ROS topic
     - ``/scan``
     - Keep ``/scan`` to minimize software changes
   * - Serial speed
     - 115200 baud
     - Update to the purchased S2 model's required baud rate
   * - Fail-safe
     - Ultrasonic sensors
     - Retain and validate

.. important:: IP rating is system-level

   An IP65 LiDAR does not make the complete installation IP65. The cable exit,
   USB/serial adapter, mounting interface, and electronics enclosure still need
   sealing and strain relief.
