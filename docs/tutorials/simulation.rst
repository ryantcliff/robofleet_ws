Simulation & Testing
====================

The code has hardware-free tests and a Gazebo simulation, so we can check
navigation changes before touching the real robot. Everything on this page
runs over SSH on the Jetson, and several of us can run it at the same time.

Quick start over SSH
--------------------

.. code-block:: bash

   ssh roboflock@<jetson-ip>
   cd ~/robofleet_ws
   scripts/sim.sh test            # every hardware-free test, about 5 minutes
   scripts/sim.sh gazebo          # robot in Gazebo with SLAM and Nav2

``scripts/sim.sh`` sources ROS and this workspace for you (``~/.bashrc`` does
not source any workspace). Each run gets its own ROS domain (20 to 80) and its
own Gazebo partition, so it never sees the real robot on domain 0 or anyone
else's run. It also gets its own log folder under ``/tmp/robofleet-sim/``.
``scripts/sim.sh list`` shows who is running what.

If you changed code, build first:

.. code-block:: bash

   source /opt/ros/humble/setup.bash
   colcon build --symlink-install --executor sequential

Navigation smoke tests
----------------------

.. code-block:: bash

   scripts/sim.sh test nav          # Nav2 with synthetic localization
   scripts/sim.sh test nav-local    # Nav2 with the local EKF
   scripts/sim.sh test nav-gps      # Nav2 with the GPS EKF
   scripts/sim.sh test beacon
   scripts/sim.sh test follow

These run the real ROS 2 navigation and localization nodes on fake sensor data.
They check startup, transform ownership, the localization flow and goal
behavior. They do not replace real-world calibration or collision testing.

The scripts also run on their own (``python3 src/bring_up/scripts/nav2_smoke_test.py``),
but then they use fixed domains and log paths, so two people running the same
test collide.

If a test reports ``FLAKY``, it stalled once and passed on retry. That happens
when two Nav2 stacks start at the same moment on the Jetson's 6 cores. A real
failure says ``FAIL``.

Unit tests
----------

.. code-block:: bash

   scripts/sim.sh test unit

This runs everything in ``src/bring_up/test`` plus
``src/urdf_description/test/test_urdf_frames.py``.
``test_diff_drive_controller.py`` uses a fake ODrive, so it cannot touch the real
motor controllers. ``test_urdf_frames.py`` pins the GPS and lidar frames the real
robot uses, so a model edit cannot move them by accident.

Gazebo
------

Gazebo Fortress (the Gazebo that goes with ROS 2 Humble) has to be installed
once by someone with ``sudo``:

.. code-block:: bash

   sudo apt install ros-humble-ros-gz ros-humble-foxglove-bridge

Then:

.. code-block:: bash

   scripts/sim.sh gazebo                 # Gazebo + SLAM + Nav2
   scripts/sim.sh gazebo nav:=false      # just the robot, drive it yourself

The script prints the domain it took, for example ``domain 23``. In a second
SSH terminal:

.. code-block:: bash

   scripts/sim.sh teleop 23     # drive with the keyboard
   scripts/sim.sh shell 23      # a shell for ros2 topic echo, ros2 node list, ...

Gazebo runs without a window (``headless``) because SSH sessions have no
display. The robot spawns at the origin of a 12 x 12 m walled yard with three
obstacles (``src/urdf_description/worlds/test_yard.sdf``).

The simulator publishes what the real drivers and EKF would: ``/scan``,
``/odometry/local`` and the ``odom -> base_link`` transform. ``slam_toolbox`` adds
``map -> odom``, and Nav2 drives ``/cmd_vel``. These are the same
``slam.launch.py`` and ``nav2.launch.py`` the robot uses.

Seeing it in a browser
~~~~~~~~~~~~~~~~~~~~~~

``sim.sh gazebo`` starts Foxglove Bridge on the Jetson, listening only on
``localhost``. It prints a tunnel command for your own computer, for example:

.. code-block:: bash

   ssh -N -L 8768:localhost:8768 roboflock@<jetson-ip>

Leave that running, open https://app.foxglove.dev, choose *Open connection*, and
connect to ``ws://localhost:8768``. Add a 3D panel to see the robot, ``/scan``
and ``/map``. You can send Nav2 goals by publishing a pose to ``/goal_pose``
from the 3D panel. The port is different for every run; use the one the script
printed.

On a computer with a screen
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   ros2 launch bring_up sim.launch.py headless:=false rviz:=true

What the simulation is not
~~~~~~~~~~~~~~~~~~~~~~~~~~

* **The model is not to scale.** The CAD meshes give 0.1825 m wheels, 0.77 m
  apart. The robot measured on 2026-09-26 has 0.125 m wheels, 0.74 m apart
  (``diff_drive_controller.py``). Distances and speeds in Gazebo are close, not
  exact.
* The Nav2 footprint is ``robot_radius: 0.22``, smaller than the chassis.
  Paths in the sim can pass closer to obstacles than the real robot can.
* The rocker-bogie joints are fixed in the URDF, so the simulated robot is rigid.
* There is no simulated IMU, GPS, ultrasonic e-stop, ODrive or beacon. Those
  paths are covered by the smoke tests above, not by Gazebo.

Test order
----------------

**Simulation, then a bench test with the wheels raised, then sensor calibration
outdoors, then a slow test in an open field with a spotter who can stop it.**
