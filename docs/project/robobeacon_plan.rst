RoboBeacon Plan
===============

The RoboBeacon is the thing a person carries so that a FleetBot follows them. Today
it is a set of parts and a wiring recipe, not an object that anybody could pick up and
use. This page says what we have, what is missing, and how we plan to get from one to
the other. Where the beacon will be used is described in :doc:`burning_man`.

Where it stands
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Piece
     - Status
     - Where it is
   * - Robot-side receiver
     - :ready:`Software present`
     - ``beacon_receiver.launch.py`` reads the HC-12 on ``/dev/ttyTHS1`` and publishes
       ``/gps/beacon/fix``.
   * - Beacon to goal pose
     - :ready:`Software present`
     - ``beacon_goalpose`` converts the fix to a ``map`` target. ``mission_manager``
       stops 3 m short and cancels when the target is stale for 3 s.
   * - Simulation
     - :ready:`Software present`
     - ``fake_beacon.py`` and ``follow_smoke_test.py``. These use fake data and are
       not a test of the real link.
   * - Beacon GPS setup
     - :ready:`Script present`
     - ``configure_beacon_gps.py`` sets the NEO-M8P to GGA only, 9600 baud, 5 Hz,
       saved to flash.
   * - Beacon parts
     - :inherited:`Inherited`
     - A SparkFun NEO-M8P-2-12 and a pair of HC-12 radios, in
       :doc:`hardware_inventory`. Wiring and radio settings are in :doc:`../concepts/communications`.
   * - Beacon firmware
     - Not needed today
     - The NEO-M8P feeds the HC-12 directly, so nothing runs on the beacon itself.
   * - Enclosure, power, switch, indicators
     - :planned:`Not built`
     - Nothing exists yet. The inherited bench wiring calls for a 5 V power bank; see :doc:`../concepts/communications`.
   * - Outdoor test of the real link
     - :planned:`Not done`
     - Listed as the next step in :doc:`roadmap`.
   * - Many robots, one beacon
     - :planned:`Not designed`
     - See below.

So the robot side of following is largely there, and the beacon side is a bench
wiring recipe. Nothing here has been tested outdoors, so none of it counts as working
until we have done that.

What we still have to settle
----------------------------

Accuracy against the stand-off
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The beacon sends ordinary GPS sentences, and the robot uses its own GPS. Our stand-off
is 1.5 to 3.0 m. Ordinary single-receiver GPS can be off by a few meters, which is the
same size as the distance we are trying to hold. We have not measured this on our
hardware. This is the most important thing to find out first, because it decides
whether the current parts are enough.

If they are not, the options to evaluate are:

* **Keep plain GPS** and accept a looser stand-off, if the measured error allows it.
* **RTK between the beacon and the robot**, where the two receivers correct each other.
  Internet corrections will not be available at the festival, so this would need the
  beacon or a base station to supply them over our own radio. We have not worked out
  which receivers support this, and that needs checking against the u-blox datasheets
  before anyone buys anything.

The radio link
~~~~~~~~~~~~~~

* The HC-12 pair is documented at about 1 km in the open, and that is a vendor claim we
  have not tested.
* The beacon sends GGA at 5 Hz on 9600 baud on a fixed channel. With one beacon and
  many robots, a single shared channel is what we want, since every HC-12 receiver on
  that channel should hear the same transmission. We have only run one receiver so
  far, so we should confirm that several receive it reliably.
* We have not confirmed that our HC-12 power setting is legal in the US. See
  :doc:`burning_man`.

Power
~~~~~

* The inherited wiring recipe feeds both modules from a 5 V power bank. Some power banks switch off when
  the load is small. We have not tested whether ours stays on with this load, or how
  long it lasts.
* Heat and cold both limit battery performance, and the beacon will be carried in the
  sun.

Making it an object
~~~~~~~~~~~~~~~~~~~

Anybody should be able to pick it up and use it. That means:

* A case that survives dust, sweat and drops, and does not trap heat.
* A switch, and indicators for power, GPS fix and radio link, so a carrier can tell when
  it is not working.
* An antenna position that works while it is carried or worn, and a strap.
* Something that makes it visible at night.
* A way to charge it and clean it.

What happens when it stops
~~~~~~~~~~~~~~~~~~~~~~~~~~

The robot already stops chasing when the beacon data goes stale (requirement R-3). Other
cases are not designed yet, for example someone setting the beacon down, handing it to
another person, or walking into a crowd.

Many robots, one beacon
~~~~~~~~~~~~~~~~~~~~~~~

The end goal is a single RoboBeacon that many FleetBots follow at the same time. That
means the beacon does not need an id or a pairing step, because every robot listens to
the same broadcast. Two things do need thought:

* **Sharing the target.** Each robot is told to stop 3 m short of the same point, so
  several robots would end up in the same place. They need different stand-off
  positions or a queuing rule. This is part of the fleet awareness work, which is not
  in this year's scope.
* **One point of failure.** If the beacon fails or goes quiet, every robot stops
  following. That makes its battery, its case and its indicators matter more.

Staged plan
-----------

1. **Agree requirements with Tom.** Who carries it, runtime on one charge, range, night
   visibility, and how a stranger starts, stops and hands it off.
2. **Bench beacon and outdoor test.** Build the beacon from the parts we have, measure
   accuracy and radio range, and decide whether plain GPS is enough.
3. **Turn it into an object.** Enclosure, power, switch, indicators, antenna and strap.
4. **Many robots, one beacon.** Check that several robots can receive the one beacon at
   the same time, and decide how they share the stand-off.
5. **Environment tests.** Dust, heat, cold and drops, using the conditions in
   :doc:`burning_man`.

Steps 1 and 2 matter most for this year's delivery. Steps 4 and 5 may belong to a
later team, and we should say so in the handoff documentation.

How we will check it
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Check
     - What we need to see
   * - Fix accuracy
     - Walk the beacon over a known path and compare the reported position to the
       real one. Record the error in meters.
   * - Radio range
     - Walk away until fixes stop arriving, and record the distance in open ground and
       among obstacles.
   * - Runtime
     - Run the beacon from a full battery until it stops, with the power bank we plan
       to use.
   * - Loss of signal
     - Cover the antenna or switch the beacon off, and watch the robot stop.
   * - Dust, heat and cold
     - Run it sealed in dust and at temperature extremes, and look for failures.
   * - Stranger test
     - Hand the beacon to somebody who has never seen it and see whether they can use it
       without help.

Open decisions
--------------

* Is plain GPS accurate enough for a 1.5 to 3.0 m stand-off? We decide this after step 2.
* How do several robots share one beacon's stand-off without colliding? This is for a
  later team.
* Which parts of this belong in this year's scope, and which are left for the next team?
