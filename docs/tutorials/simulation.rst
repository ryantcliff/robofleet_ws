Simulation & Testing
====================

The current codebase includes hardware-free integration tests so navigation
changes can be validated before touching the physical robot.

Navigation smoke tests
----------------------

.. code-block:: bash

   python src/bring_up/scripts/nav2_smoke_test.py
   python src/bring_up/scripts/nav2_smoke_test.py --localization local
   python src/bring_up/scripts/nav2_smoke_test.py --localization gps
   python src/beacon_pkg/scripts/beacon_smoke_test.py
   python src/bring_up/scripts/follow_smoke_test.py --beacon-speed 1.2

These tests exercise real ROS 2 navigation/localization nodes with synthetic
sensor inputs. They validate startup, TF ownership, localization flow, and goal
behavior; they do not replace real-world calibration or collision testing.

Unit tests
----------

.. code-block:: bash

   python3 -m pytest \
     src/bring_up/test/test_e_stop.py \
     src/bring_up/test/test_gps_monitor.py \
     src/bring_up/test/test_mission_manager.py \
     src/bring_up/test/test_meshtastic_bridge.py \
     src/bring_up/test/test_ultrasonic_estop.py \
     src/bring_up/test/test_bno085_imu.py

Recommended workflow
--------------------

**Simulation -> bench test with wheels raised -> sensor calibration outdoors ->
low-speed open-field test with a spotter and physical e-stop control.**
