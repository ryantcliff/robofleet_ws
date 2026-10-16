Beacon Following
================

Beacon following is a primary 2026-2027 requirement. The person carries the
**RoboBeacon**; the robot being delivered this year is a **FleetBot**. RoboFleet
converts the received RoboBeacon latitude/longitude into a Nav2 target and
follows while maintaining a safe stand-off distance.

Data flow
---------

::

   NEO-M8P RoboBeacon --> HC-12 radio --> /gps/beacon/fix
                                             |
                                             v
                                      beacon_goalpose
                                             |
                                             v
                                      mission_manager
                                             |
                                             v
                                           Nav2

Required behavior
-----------------

**Follow**
   The formal acceptance range is approximately **1.5-3.0 m short of the
   RoboBeacon**. The current mission configuration targets 3 m, which is within
   that required range.

**Stale target**
   Cancel the Nav2 goal and stop pursuit when RoboBeacon position data becomes
   stale or unavailable.

**Obstacle-aware motion**
   Continue to use the LiDAR/Nav2 stack so a known obstacle in the planned path
   is represented and the FleetBot does not intentionally drive through it.

**Safety**
   Final velocity still passes through operator e-stop/arming and command
   arbitration before motor control.

Return-home status
------------------

Return-home and Meshtastic features may be preserved or improved, but they are
not required for this year's final acceptance unless the requirements document
is formally revised.

Simulation
----------

.. code-block:: bash

   ros2 launch bring_up bringup.launch.py \
     follow:=true slam:=false hardware:=false sim:=true
