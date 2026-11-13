RoboBeacon Outdoor Test
=======================

This is the checklist for our first outdoor test of the RoboBeacon. It answers the
questions in step 2 of :doc:`robobeacon_plan`: does the beacon get a GPS fix, is plain
GPS accurate enough for our 1.5 to 3.0 m stand-off, and how far does the HC-12 link
reach. One visit of about 30 to 45 minutes covers all of it.

We ran it on 2026-11-13. The results are at the end of this page. They come from one site and
about an hour, so we treat them as a first look and not as final numbers.

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

How we ran it
~~~~~~~~~~~~~

The robot stayed in one place with its receiver running and its own GPS logging at 1 Hz.
We recorded the beacon's fixes on the robot, and marked each phase by hand. We carried the
whole beacon on a laptop held at chest height, with the GPS antenna on top of it. We could
only measure 27 ft 9 in (8.46 m) on the ground, so point B is 8.46 m from point A and not
10 m. Sky conditions were 8 to 10 satellites, with an HDOP between 1.8 and 4.4.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Check
     - Result
     - Notes
   * - Antenna used
     - Not recorded
     - We did not write down whether it was RF-015 or RF-017.
   * - Time to first fix
     - Not timed
     - A fix was already present at our first check.
   * - Wander while still
     - 95% of fixes within 1.2 to 4.6 m of the average
     - Four 2-minute windows. Largest drift 5.9 m inside one window.
   * - Same spot, two windows
     - 3.3 m apart at A, 4.0 m apart at B
     - The averages of two windows at the same marked spot.
   * - A to B distance (true 8.46 m)
     - 6.4 to 12.3 m
     - Errors from -2.1 to +3.9 m across four pairings of the still windows.
   * - Walk A to B (true 8.46 m)
     - 7.92 m, error -0.54 m
     - The only walk with a healthy link, with 40 fixes at the end point.
   * - Fixes per second while walking
     - 4.9
     - After we secured a loose connector. It was as low as 1.5 before.
   * - Robot to beacon at 3.0 m
     - Mean 3.74 m, wander 1.27 m (1 std)
     - Ranged from 2.49 to 7.06 m over 143 s.
   * - Robot to beacon at 6.0 m
     - Mean 4.99 m, wander 0.79 m (1 std)
     - Ranged from 3.75 to 5.87 m over 128 s.
   * - Range where fixes stop
     - Not tested
     - We did not have the space.

Radio link
~~~~~~~~~~

Our first walks lost most of the radio data. The fix rate fell from 5 per second to as low as
1.5 per second, and damaged sentences rose, mostly after we stopped moving. Moving the HC-12
to the top of the laptop with its antenna vertical did not help. Then a jumper between the
NEO-M8P and the HC-12 came loose, and after we secured the connectors one walk gave
4.9 fixes per second with no gaps and two damaged sentences in 47 seconds.

We think the loose connector was the cause, because it fits the damaged sentences and the
timing. We have not reproduced the fault on purpose, and we have only one walk since the fix.
The final beacon needs soldered or locking connectors, and not jumper wires.

Standing still
~~~~~~~~~~~~~~

In every still window the position stayed within about 1 to 2 m for a couple of minutes, and
then moved. At point A the average of the first window was 5.9 m from the average of its last
fifth. Two windows at the same marked spot gave averages 3.3 m apart, and at B 4.0 m apart.
So the position holds for a minute or two but wanders by several meters over longer times.

Walking
~~~~~~~

Only the last walk had a healthy radio link, and it read 7.92 m for a true 8.46 m. The path
stayed within 0.45 m of a straight line (RMS). Three earlier walks had too few fixes at the end
points to judge, and we threw out one because we marked its start late. One clean walk is not
enough to say whether the beacon reads short while moving.

Robot to beacon
~~~~~~~~~~~~~~~

This is the distance the follow logic would see. We paired each robot fix with the average of
the beacon fixes within half a second, and compared the distance between them with the true
distance. The robot's ZED-F9P was running on GPS and GLONASS only at 1 Hz, from our
2026-10-02 field notes, and we did not recheck that today.

* At 3.0 m, the reported distance averaged 3.74 m and wandered by 1.27 m (1 std).
* At 6.0 m, it averaged 4.99 m and wandered by 0.79 m.
* The two receivers' errors did not cancel. The difference wandered more than either
  receiver alone, mostly in the north-south direction.
* The two windows were at different bearings from the robot, so we compared them by distance.

What we did not test
~~~~~~~~~~~~~~~~~~~~

* Radio range.
* What the robot does when the beacon goes quiet, on real hardware (R-3).
* Several robots receiving one beacon.
* A second site, another time of day, night, or dust.
* RTK.

How to read the results
~~~~~~~~~~~~~~~~~~~~~~~

The stand-off we owe is 1.5 to 3.0 m. The errors we measured, from 1 to 4 m, are the same
size, so plain GPS on both ends looks marginal at best for holding it. This is one site and
one day. Before we decide, we should repeat the test at another time and place, and evaluate
RTK, as described in :doc:`robobeacon_plan`. We have not set a formal threshold, and the
numbers are for the team to judge.
