Burning Man
===========

The place this robot is for is the Burning Man festival. Our client, Tom, wants
to bring a FleetBot to Black Rock City so that he, or anybody else, can carry the
**RoboBeacon** and have the FleetBot follow them. This page collects what we know
about that environment and what it means for the robot. We use it to decide what
to build, what to test, and what we still have to ask.

.. note:: How we label what we know

   **Official** means it comes from a Burning Man Project page. **Reported** means
   it comes from news or a third party. **Ours** means it is our own reasoning from
   the repo or from what Tom told us. We found nothing in any source that mentions
   robots specifically, so every rule below is a general one that we apply to the
   FleetBot. Please do not read any of it as a ruling on whether the FleetBot is
   allowed.

The event
---------

* **When:** August 29 to September 6, 2027. The theme is Spellbound. (Official)
* **Where:** the Black Rock Desert in northern Nevada, near Gerlach, about 120
  miles north of Reno, at nearly 4,000 feet. (Official and reported)
* **Who:** tens of thousands of people. Third-party sources say 70,000 to 80,000.
  We did not find an official headcount. (Reported)
* **Connected to us:** our final delivery is no later than **April 1, 2027**, so
  the event is about five months after we hand the robot over.

Weather and ground
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 45 35

   * - Condition
     - What we found
     - Source type
   * - Dust
     - The surface contains alkaline gypsum and silica dust. It gets into camera
       lenses, laptop fans and alternators. Compressed air at low pressure is the
       usual way to clean electronics, and water is avoided.
     - Official, plus a DJ-gear site for the cleaning advice
   * - Wind
     - Often 20 to 30 mph. Storms bring 40 to 70 mph, and gusts can exceed 75 mph.
       Dust storms can arrive within minutes.
     - Official, plus news reports
   * - Whiteouts
     - Burning Man's advice is to stop where you are and wait, with a mask and
       goggles. Prolonged whiteouts are called unlikely, but you should be prepared
       for them. How long they last is disputed (15 to 30 minutes versus hours).
     - Official, duration unverified
   * - Heat
     - Daytime temperatures routinely exceed 100 F, with very low humidity.
     - Official
   * - Cold
     - Pre-dawn temperatures can approach freezing. Daily swings of 40 degrees or
       more are reported.
     - Official and reported
   * - Rain
     - Rare, but it happens. In 2023 about 0.8 inch fell in 24 hours. Organizers
       stopped all vehicle movement on the playa because the mud made driving
       impossible.
     - Reported

Rain and wind: what Tom told us
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tom told us that the robot is **not expected to move in rain or in really windy
conditions**. Wind kicks up dust that makes it very hard to see. Rain turns the
dust on the ground into thick mud that builds up on the wheels and stops motion.
We did not find a source that describes mud caking on wheels, so this comes from
Tom. It matches what happened in 2023.

We are recording this as **client guidance**, not as a formal requirement. It is
not yet in :doc:`requirements`, and we have not changed R-6. The two do not
conflict: R-6 is about protecting the robot, and Tom's rule is about when it
should drive. For now we handle it by procedure. An operator stops the robot with
the existing ``stop`` command, the PS4 Cross button, or by pulling the XT90.

Two things this leaves open, which we should raise with Tom:

* Nothing on the robot detects wind, rain or heavy dust. If anybody can carry the
  RoboBeacon, there may be nobody trained watching the weather. An automatic weather
  hold is something we could add later, but it is outside our scope today.
* Where does the robot wait out a storm? R-6 does not cover unattended severe
  weather, and a parked robot still sits in the dust.

Rules that touch a robot
------------------------

* **Licensing.** Burning Man's permit with the Bureau of Land Management says every
  vehicle driven at the event has to be licensed by Burning Man through its
  Department of Mutant Vehicles. Applications run roughly from February to mid-April,
  and acceptance is not guaranteed. We found no rule that says whether a small
  autonomous robot counts as a vehicle. **This could land in the same weeks as our
  April 1 delivery.** Tom needs to ask the Burning Man DMV, using the current year's
  handbook.
* **Speed.** The limit is 5 mph (about 2.2 m/s) in the city, and the Survival Guide
  lists 10 mph on Gate Road. Our Nav2 configuration caps at 1.2 m/s, which is under
  that limit. The 10 mph figure comes from an older guide.
* **Right of way.** Pedestrians, bicycles and emergency vehicles always have it.
* **Night.** Vehicles driving in and out of the event need working head, tail and
  brake lights, and mutant vehicles are held to their own lighting criteria. We do
  not know which set would apply to the FleetBot. Either way, a robot moving among
  walkers and bikes in the dark needs its own lights.

Radio, GPS and connectivity
---------------------------

* **Cell and internet.** There is no dependable cell service and no public
  internet. The few temporary towers have been overloaded. GPS itself works, because
  it does not need a network. Our follow chain (GPS, HC-12, Nav2) and the Meshtastic
  home station do not need internet, which is good. Anything that downloads
  corrections or maps on the fly will not work.
* **RTK corrections** from an internet service would not be available, so any
  higher-accuracy plan has to bring its own base or run without one. See
  :doc:`robobeacon_plan`.
* **Licensed channels.** Burning Man Project holds licensed radio channels for its
  own use. One emergency channel is open to anyone for real emergencies only.
  Participants are responsible for following FCC rules for their own radios.
* **Our radios.** The HC-12 modules are 433 MHz and default to a maximum power of
  100 mW. We have **not** confirmed what the United States allows on that band for
  this kind of link (47 CFR 15.231 is where to look). A third-party article from
  September 2026 also reports that the default Meshtastic settings in the US may
  not comply with FCC rule 15.247. We have not checked either one against the
  rules, so treat both as open items.

People and crowds
-----------------

The city is dense and busy, with walkers, bikes, e-bikes and art cars in the same
space, much of it at night. Our follow target is 3 m and the stand-off range is 1.5
to 3.0 m. The FleetBot's LiDAR, ultrasonic brake and e-stop are what keep it from
hitting people. We do not yet know the robot's final weight or whether there is a
limit on mass or size for an unlicensed machine.

What this means for each part of the robot
------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Part
     - Concern at Burning Man
     - What we should check
   * - Drivetrain and wheels
     - Alkaline dust in bearings and ODESCs, and mud that stops the wheels.
     - Sealed or shielded bearings, cleaning access, and a plan to stay parked in rain.
   * - Enclosures and cooling
     - Fine dust gets into anything with a fan or a gap. Heat over 100 F with sealed
       boxes, and cold near freezing before dawn.
     - Hot and cold checks on the Jetson and the motor electronics, with the
       enclosure sealed. The current weatherproofing page only lists a heat check.
   * - LiDAR (RPLIDAR S2, IP65)
     - Dust in the air produces false obstacles and can hide real ones. An IP65 case
       keeps dust out but does not let the beam see through a dust cloud.
     - Test in blowing dust, and consider filtering returns that look like particles.
       Coating on the window needs cleaning.
   * - Ultrasonic sensors
     - Dust and wind noise on the sensors. Sensors that go quiet already block
       forward motion in follow mode.
     - Check that dust does not make them fail closed all the time.
   * - GPS and heading
     - Open sky helps. A standalone beacon fix may be no more accurate than our
       stand-off distance.
     - Measure real beacon accuracy outdoors. See :doc:`robobeacon_plan`.
   * - Radios
     - Range and regulation, and crowds of other radios on shared bands.
     - Range test at event scale, and a check of power limits.
   * - Battery and power
     - Heat and cold limits on charging and discharge.
     - Find the battery's temperature limits and a place for it out of the sun.
   * - Stopping
     - Crowds. The only hard stop today is pulling the XT90.
     - A physical stop an untrained person can reach, which is already an open item
       in :doc:`electrical_review`.

Beyond this year: a fleet
-------------------------

RoboFleet is meant to become many FleetBots, each following its own RoboBeacon, and
they will eventually need to know about each other and plan around each other. That
is not in our scope. We note it so that what we build does not make it harder:

* Nav2 does not include multi-robot traffic handling. Its maintainers have said the
  field is not mature enough to include. Options people use are Open-RMF, or a
  simple wait-and-signal scheme. Per-robot namespaces are the common starting point.
* Today our topics and frames are fixed names, such as ``/cmd_vel`` and
  ``/gps/beacon/fix``, so two robots on one network would collide. Using a robot id
  or namespace parameter would be the first step.
* The RoboBeacon sends plain GPS sentences with no id, and the robot cannot tell which
  beacon is which. See :doc:`robobeacon_plan` for pairing.
* A robot treating another robot as a moving obstacle in its costmap is the simplest
  form of awareness. Sharing each robot's position over a link is the next step.

Open questions
--------------

For Tom:

* Who is allowed to carry the RoboBeacon, and for how long at a time?
* How will the robot be stored and protected during a storm?
* Does he expect the robot to operate at night?
* Has he already asked the Burning Man DMV about the robot?

For us:

* Does the HC-12 setup meet the US limits for the 433 MHz band?
* How well does the RPLIDAR S2 do in blowing dust?
* Should the robot stop automatically in high wind, rain or heavy dust?

Sources
-------

* `Burning Man 2027 event page <https://burningman.org/?p=4383>`__
* `Burning Man weather page <https://burningman.org/black-rock-city/preparation/playa-living/weather/>`__
* `Burning Man survival guide <https://survival.burningman.org/survival-health-and-safety/survival/>`__
* `Burning Man event FAQ <https://burningman.org/black-rock-city/preparation/faq/>`__
* `Vehicle rules and protocols <https://burningman.org/black-rock-city/bring-your-mutant-vehicle/vehicle-rules-and-protocols/>`__
* `Vehicles and driving, Survival Guide <https://survival.burningman.org/getting-around-brc/vehicles-driving/>`__
* `2023 rain and mud (NPR) <https://www.npr.org/2023/09/02/1197441202/burning-man-festival-rains-floods-stranded-nevada>`__
* `Participant emergency reporting, 2026 <https://burningman.org/wp-content/uploads/2026/08/BRC-Participant-Emergency-Reporting-2026.08.05.pdf>`__
* `FCC ISM rules and LoRa mesh (Hackaday, 2026) <https://hackaday.com/2026/09/17/fcc-ism-rules-may-shatter-lora-mesh-communities/>`__
* `Nav2 Route Server discussion <https://discourse.ros.org/t/nav2-request-for-comment-route-server/28410/14>`__
* `Open-RMF traffic management interfaces <https://discourse.openrobotics.org/t/traffic-management-interfaces-for-the-next-generation/44414/>`__
* `LiDAR disturbances by airborne particles <https://arxiv.org/pdf/2105.04193>`__
