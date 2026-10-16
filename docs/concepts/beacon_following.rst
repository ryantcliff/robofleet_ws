Beacon Following
================

Beacon following is a primary requirement for the 2026–2027 team. The person
carries a GNSS beacon; RoboFleet converts the received latitude/longitude into
a Nav2 target and follows while maintaining a stand-off distance.

Data flow
---------

::

   NEO-M8P beacon --> HC-12 radio --> /gps/beacon/fix
                                         |
                                         v
                                  beacon_goalpose
                                         |
                                         v
                                  mission_manager
                                         |
                                         v
                                       Nav2

Behavior
--------

**Follow**
   Target the beacon and stop approximately 3 m short.

**Home**
   Navigate toward the latest home-station position and stop approximately
   1.5 m short.

**Stale target**
   Cancel the Nav2 goal when position data becomes stale.

**Safety**
   Final velocity still passes through joystick e-stop and command arbitration
   before motor control.

Simulation
----------

.. code-block:: bash

   ros2 launch bring_up bringup.launch.py \
     follow:=true slam:=false hardware:=false sim:=true
