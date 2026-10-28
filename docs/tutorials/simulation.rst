Simulation & Testing
====================

The code has hardware-free tests, so we can check navigation changes before
touching the real robot.

Navigation smoke tests
----------------------

.. code-block:: bash

   python src/bring_up/scripts/nav2_smoke_test.py
   python src/bring_up/scripts/nav2_smoke_test.py --localization local
   python src/bring_up/scripts/nav2_smoke_test.py --localization gps
   python src/beacon_pkg/scripts/beacon_smoke_test.py
   python src/bring_up/scripts/follow_smoke_test.py --beacon-speed 1.2

These run the real ROS 2 navigation and localization nodes on fake sensor data.
They check startup, transform ownership, the localization flow and goal
behavior. They do not replace real-world calibration or collision testing.

Unit tests
----------

.. code-block:: bash

   python3 -m pytest \
     src/bring_up/test/test_diff_drive_controller.py \
     src/bring_up/test/test_e_stop.py \
     src/bring_up/test/test_gps_monitor.py \
     src/bring_up/test/test_mission_manager.py \
     src/bring_up/test/test_meshtastic_bridge.py \
     src/bring_up/test/test_ultrasonic_estop.py \
     src/bring_up/test/test_bno085_imu.py

``test_diff_drive_controller.py`` uses a fake ODrive, so it cannot touch the real
motor controllers.

Test order
----------------

**Simulation, then a bench test with the wheels raised, then sensor calibration
outdoors, then a slow test in an open field with a spotter who can stop it.**
