RoboBeacon Outdoor Test
=======================

This is the checklist for our first outdoor test of the RoboBeacon. It answers the
questions in step 2 of :doc:`robobeacon_plan`: does the beacon get a GPS fix, is plain
GPS accurate enough for our 1.5 to 3.0 m stand-off, and how far does the HC-12 link
reach. One visit of about 30 to 45 minutes covers all of it.

We have not run this test yet. Every result below is blank until someone fills it in.

What we already know
--------------------

On the bench, indoors, we checked these:

* The NEO-M8P-2 on ``/dev/ttyACM6`` is configured: GGA only, 9600 baud, 5 Hz.
* The wiring works. The robot's HC-12 delivers about 5 sentences per second, and the
  sentences arrive intact.
* Indoors the beacon reports fix quality ``0`` and ``00`` satellites. That is what we
  expect without a view of the sky. The coordinates it prints indoors are a stored
  last-known position, not a fix.
* When the beacon was out of range the robot's HC-12 received 0 bytes, so no data on
  that port means no radio link.

We have not seen a real fix, measured accuracy, or measured range.

Before you go out
-----------------

* [ ] The power bank is charged, and it is not one that shuts off at a small load.
* [ ] The beacon is wired as in the README, the HC-12 antenna is attached, and the
  GNSS antenna is connected. Note which antenna you used (RF-015 or RF-017).
* [ ] The robot is powered and its HC-12 is connected to ``/dev/ttyTHS1``.
* [ ] You have a tape measure, something to mark the ground, a way to write results
  down, and a second person if possible.
* [ ] The robot stays in one place for the whole test. The test does not need the
  wheels to move. Do not start follow mode on the real robot.

On the robot, start the receiver. The drive service does not start it for us:

.. code-block:: bash

   source /opt/ros/humble/setup.bash && source ~/robofleet_ws/install/setup.bash
   ros2 launch beacon_pkg beacon_receiver.launch.py

1. Get a fix
------------

Put the GNSS antenna flat, facing the sky, away from walls and trees. Stand still.
Wait up to 5 minutes.

Check the fix with:

.. code-block:: bash

   ros2 topic echo /gps/beacon/fix --once

* [ ] ``status`` is ``0`` or higher, and latitude and longitude are not ``0.0``.
* [ ] Record the minutes it took to get the first fix.

``status: -1`` means no fix. The robot ignores no-fix messages, so they cannot send it
to ``0.0, 0.0``. This comes from the code in ``beacon_goalpose``, and we have not tested
it with a real no-fix stream.

If nothing arrives at all, you are probably out of radio range. Move closer to the
robot and read the raw port to confirm:

.. code-block:: bash

   timeout 6 cat /dev/ttyTHS1 | head -c 400

2. Accuracy standing still
--------------------------

Mark point A on open ground. Hold the beacon at chest height on the mark, and keep it
still for 2 minutes while recording:

.. code-block:: bash

   ros2 topic echo /gps/beacon/fix --csv > ~/beacon_A.csv

Mark point B exactly 10 m from A with the tape. Repeat the 2 minute recording at B:

.. code-block:: bash

   ros2 topic echo /gps/beacon/fix --csv > ~/beacon_B.csv

* [ ] How much does the reported position wander at A while the beacon is still?
* [ ] What distance do the reported positions give between A and B? The true value
  is 10 m.

3. Accuracy while walking
-------------------------

Mark a straight line of 20 m. Walk it at a normal pace with the beacon at chest height,
and record:

.. code-block:: bash

   ros2 topic echo /gps/beacon/fix --csv > ~/beacon_walk.csv

* [ ] Does the reported path look like the line you walked?
* [ ] How many fixes per second arrived while you walked?

4. Radio range
--------------

Leave the robot where it is. Walk away in a straight line over open ground, and stop
every 25 m for 10 seconds. At each stop, check the fix rate on the robot:

.. code-block:: bash

   ros2 topic hz /gps/beacon/fix

* [ ] Record the distance and the rate at each stop.
* [ ] Record the distance where the rate drops a lot or the fixes stop.
* [ ] Walk back and confirm the link recovers.

Measure distances with the beacon's own fixes only if the accuracy test shows they are
good enough. Otherwise pace it out or use a measuring wheel.

Results
-------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Check
     - Result
     - Notes
   * - Antenna used
     -
     -
   * - Time to first fix
     -
     -
   * - Wander while still (point A)
     -
     -
   * - A to B distance (true 10 m)
     -
     -
   * - Fixes per second while walking
     -
     -
   * - Range where fixes stop
     -
     -

How to read the results
-----------------------

The stand-off we owe is 1.5 to 3.0 m. If the wander and the 10 m error are well below
that, plain GPS may be enough. If they come close to 1.5 m or more, we should evaluate
RTK, as described in :doc:`robobeacon_plan`. We have not set a formal threshold, and
the numbers are for the team to judge once we have them.

If the fix never arrives outdoors, the first suspect is the antenna, because the
cabling of the two antennas is unconfirmed in :doc:`hardware_inventory`.
