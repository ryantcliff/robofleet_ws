RoboFleet Documentation
=======================

**RoboFleet** is the 2026-2027 continuation of the autonomous rover previously
known as **RoboFlock**. The current team is building on the inherited mechanical
and ROS 2 platform rather than restarting from scratch.

The broader RoboFleet concept is a group of **FleetBots** able to follow a
designated GPS **RoboBeacon**. The required 2026-2027 delivery is one working
FleetBot that reliably follows the RoboBeacon outdoors while meeting the formal
safety and weather-protection requirements.

Project lineage
---------------

**Project Dust Runners**
   Earlier distributed-control prototype using multiple microcontrollers and UWB tracking.

**RoboFlock**
   Transitioned to a Jetson-centered ROS 2 architecture with GPS tracking,
   LiDAR, Nav2, and expanded project documentation.

**RoboFleet - 2026-2027**
   Continues the inherited platform with emphasis on RoboBeacon following,
   absolute heading, obstacle-aware navigation, supervised weather protection,
   safety verification, and reproducible handoff documentation.

System snapshot
---------------

* **NVIDIA Jetson Orin Nano** :inherited:`Inherited` - retained as the ROS 2
  compute platform; a compute upgrade is outside the current budget.
* **GPS beacon following** :ready:`Software path present` - FleetBot and
  RoboBeacon GNSS positions are converted into map-frame targets.
* **BNO085 IMU** :planned:`Required upgrade` - the current branch includes
  BNO085 support so fused magnetic heading can replace the inherited fixed-yaw behavior.
* **RPLIDAR S2 30 m** :planned:`Planned upgrade` - IP65 replacement for the
  inherited A1-class scanner.
* **Weather protection** :planned:`Formal requirement` - supervised light rain,
  incidental splashes, and wind-carried alkaline dust; no complete-robot IP claim.

Architecture at a glance
------------------------

::

   RoboBeacon GPS --> HC-12 / GPS fix --> goal pose --------------+
                                                                  |
   FleetBot GPS ------+                                           v
   BNO085 IMU --------+--> robot_localization --> Nav2 --> safety / command mux --> ODrive motors
   RPLIDAR / RF2O ----+

.. important:: Documentation philosophy

   This site intentionally distinguishes **inherited**, **implemented/software
   ready**, and **planned** work. A documented feature should not be interpreted
   as fully commissioned on the physical robot unless its page explicitly says so.

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
