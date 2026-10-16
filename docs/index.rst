RoboFleet Documentation
=======================

**RoboFleet** is the 2026–2027 continuation of the autonomous rover previously
known as **RoboFlock**. The current team is building on the inherited mechanical
and ROS 2 platform rather than restarting from scratch.

The current engineering focus is dependable GPS beacon following,
weather-resistance, hardware reliability, and a repeatable path from simulation
to real-robot commissioning.

Project lineage
---------------

**Project Dust Runners**
   Earlier distributed-control prototype using multiple microcontrollers and UWB tracking.

**RoboFlock**
   Transitioned to a Jetson-centered ROS 2 architecture with GPS tracking,
   LiDAR, Nav2, and expanded project documentation.

**RoboFleet — 2026–2027**
   Continues the inherited platform with emphasis on beacon following,
   weatherproofing, sensor reliability, and commissioning the autonomy stack.

System snapshot
---------------

* **NVIDIA Jetson Orin Nano** :inherited:`Inherited` — runs Ubuntu 22.04,
  ROS 2 Humble, Nav2, ``robot_localization``, and custom project nodes.
* **GPS beacon following** :ready:`Software path present` — robot and beacon
  GNSS positions are converted into map-frame targets for autonomous tracking.
* **BNO085 IMU** :planned:`Planned hardware` — the current branch includes a
  BNO085 driver so fused magnetic heading can replace the inherited IMU.
* **Weather-resistant LiDAR** :planned:`Planned hardware` — the team plans to
  replace the exposed A1-class scanner with an IP-rated RPLIDAR.

Architecture at a glance
------------------------

::

   Beacon GPS --> HC-12 / GPS fix --> goal pose ------------------+
                                                                  |
   Robot GPS --------+                                            v
   BNO085 IMU -------+--> robot_localization --> Nav2 --> twist_mux / e-stop --> ODrive motors
   LiDAR / RF2O -----+

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
