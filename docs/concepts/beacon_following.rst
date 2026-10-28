Beacon Following
================

Following the beacon is the main thing we have to deliver. A person carries the
**RoboBeacon**, and the **FleetBot** takes its latitude and longitude, turns it
into a Nav2 target, and follows while keeping a safe distance.

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

What it has to do
-----------------

**Follow**
   Stop about **1.5 to 3.0 m short of the RoboBeacon**. Our mission config aims
   for 3 m, which is inside that range.

**Stale target**
   If the RoboBeacon position goes stale or disappears, cancel the Nav2 goal
   and stop chasing it.

**Obstacles**
   Keep using the LiDAR and Nav2 so an obstacle in the planned path shows up
   and the FleetBot does not drive into it on purpose.

**Safety**
   The final velocity still goes through the operator e-stop and the command
   mux before it reaches the motors.

Return home
-----------

The return-home and Meshtastic features are still in the code and we may keep
improving it, but it is not required this year unless the requirements get
formally changed.

Simulation
----------

.. code-block:: bash

   ros2 launch bring_up bringup.launch.py \
     follow:=true slam:=false hardware:=false sim:=true
