RoboFleet Documentation
=======================

RoboFleet is our 2026-2027 continuation of **RoboFlock**, the autonomous rover
built by the previous team. We kept the chassis and the ROS 2 software, and we
are validating, repairing and extending them rather than starting over.

The long-term idea is a group of **FleetBots** that each follow a person
carrying a GPS **RoboBeacon**. What we owe our client this year is narrower: one
FleetBot that follows the RoboBeacon outdoors, can be stopped by an operator,
and tolerates light rain and dust.

Where the project came from
---------------------------

**Project Dust Runners**
   The earliest prototype. It used several microcontrollers and UWB tracking.

**RoboFlock**
   Moved to a Jetson running ROS 2, with GPS tracking, LiDAR, Nav2 and
   expanded documentation.

**RoboFleet (2026-2027)**
   Our work. We are focused on RoboBeacon following, a magnetometer-based
   heading, obstacle avoidance, weather protection, verifying the safety
   systems, and documentation the next team can build on.

Where things stand
------------------

* **NVIDIA Jetson Orin Nano** :inherited:`Inherited`. We are keeping it as the
  ROS 2 computer; a compute upgrade is outside our budget.
* **GPS beacon following** :ready:`Software path present`. The FleetBot's and
  the RoboBeacon's GPS positions are converted into targets in the map frame.
* **BNO085 IMU** :planned:`Required upgrade`. The current code supports it, so
  a magnetic heading can replace the fixed yaw the inherited MPU-6050 produces.
* **RPLIDAR S2 30 m** :planned:`Planned upgrade`. An IP65 scanner to replace the
  RPLIDAR A1 we have now.
* **Weather protection** :planned:`Formal requirement`. Supervised light rain,
  splashes and wind-blown alkaline dust. We are not claiming an IP rating for the
  whole robot.

How the pieces fit together
---------------------------

::

   RoboBeacon GPS --> HC-12 / GPS fix --> goal pose --------------+
                                                                  |
   FleetBot GPS ------+                                           v
   BNO085 IMU --------+--> robot_localization --> Nav2 --> safety / command mux --> ODrive motors
   RPLIDAR / RF2O ----+

.. important:: How to read these pages

   We split things into **inherited** (came with the robot), **software ready**
   (the code exists) and **planned** (not built or bought yet). Code that
   exists is not the same as something that works on the real robot, so a page
   only says a feature works if we tested it on the robot.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting_started/index

.. toctree::
   :maxdepth: 2
   :caption: Concepts

   concepts/index

.. toctree::
   :maxdepth: 2
   :caption: Construction

   construction/index

.. toctree::
   :maxdepth: 2
   :caption: Tutorials

   tutorials/index

.. toctree::
   :maxdepth: 2
   :caption: Project

   project/index
