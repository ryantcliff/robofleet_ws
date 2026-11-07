Beacon Following
================

Following the beacon is our main deliverable. A person carries the
**RoboBeacon** and a single **FleetBot** must follow at a safe stand-off.
The required band is 1.5–3.0 m; the software currently targets 3 m.

Data flow
---------

.. code-block:: text

   NEO-M8P GPS -> HC-12 -> /gps/beacon/fix -> beacon_goalpose
                                                    |
                                                    v
                                            mission_manager
                                                    |
                                                    v
                                                   Nav2

`beacon_goalpose` converts latitude/longitude into a map-frame goal
using navsat `/fromLL`. The code pulls distant targets inward so goals
remain in the rolling local planning area. `mission_manager` selects
follow/home/idle, cancels a follow goal when its target is stale (about
3 seconds) or its mode changes, and publishes status.

Requirements and status
-----------------------

* **Follow:** settle approximately 1.5–3.0 m short of the beacon.
* **Loss of data:** stop pursuit and cancel the goal when data go stale.
* **Obstacle awareness:** use LiDAR and Nav2 for route planning.
* **Operator stop:** commanded motion passes through the
  :doc:`control_safety` chain.
* **Status:** software path exists; outdoor end-to-end verification
  has not yet been documented.

Hardware launch (not a safe no-power test)
-----------------------------------------

.. warning::

   The following commands connect to real sensors and, when
   `follow:=true` is used, bring up the motor-control stack.
   Do **not** run these on a powered FleetBot until the electrical
   hazards and operator-stop procedure have been reviewed. See
   :doc:`../project/electrical_review`.

.. code-block:: bash

   ros2 launch bring_up bringup.launch.py follow:=true slam:=false

Optional Meshtastic home station:

.. code-block:: bash

   ros2 launch bring_up bringup.launch.py \
     follow:=true slam:=false station:=true

The historical home node ID defaults to `!6c743480`. Return-home
is inherited code, not required for the current delivery.

Hardware-free simulated follow
------------------------------

.. code-block:: bash

   ros2 launch bring_up bringup.launch.py \
     follow:=true slam:=false hardware:=false sim:=true

This uses a fake robot and beacon with real navigation/localization
nodes. It does not establish real GPS accuracy, antenna calibration,
radio reliability, safe braking or obstacle avoidance.

Mode commands, radio IDs and beacon wiring are documented at
:doc:`communications`. Real-world acceptance is defined by
:doc:`../project/requirements`.
