Motion command flow and operator safety
=======================================

This page documents the intended ROS 2 control chain, as implemented in
``src/bring_up/launch/bringup.launch.py``. It does not certify that the
hardware provides a safety-rated stop.

.. code-block:: text

   Nav2 /cmd_vel ---------+
                         +--> twist_mux --> /cmd_vel_mux --> ultrasonic_estop
   PS4 /cmd_vel_joy ------+                                     |
                                                              v
                                                        /cmd_vel_safe
                                                              |
                                     e_stop / arming ---------+---> diff_drive_controller
                                                                    |
                                                                    v
                                                           four ODESC controllers

Safety and motion components
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 23 77

   * - Component
     - Implemented behavior
   * - ``twist_mux``
     - Selects Nav2 or PS4 joystick velocity; joystick commands have priority.
   * - ``ultrasonic_estop``
     - Blocks **forward** motion for near or stale front-sonar measurements.
       Defaults include a 0.5 m obstacle threshold and fail-closed handling.
       Turning and reverse are still permitted.
   * - ``e_stop``
     - PS4 Cross stops; Options arms; loss of controller messages for about
       0.5 s commands a software stop.
   * - ``diff_drive_controller``
     - Consumes ``/cmd_vel_safe``, idles on software e-stop and commands zero
       after about 0.5 s without a valid motion command.

Refer to :doc:`obstacle_detection` for the sensor-specific logic and
:doc:`../tutorials/topics` for the ROS topics.

Important limits
----------------

* **There is no verified physical motor-power emergency cutoff.**
  The inherited design relies on disconnecting the motor battery to remove
  motor power. A software e-stop can leave the wheels coasting.
* The pack charges to 29.4 V and inspected controller MOSFETs are rated
  30 V absolute maximum. Read :doc:`../project/electrical_review`.
* The inherited system reportedly drove for more than 30 minutes with its
  electronics connected. That confirms prior operation in those conditions,
  not adequate transient/regen voltage margin.
* Do **not** interpret ROS safety-node test passes as a safe-to-drive signoff.

Verification order
------------------

First review power and wiring, then test ROS behavior without motors,
then plan supervised wheels-off-ground tests only after addressing the
power/safety risks, and only then consider controlled outdoor testing.
See :doc:`../tutorials/commissioning`.
