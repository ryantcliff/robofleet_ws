Installation & Build
====================

RoboFleet continues to use the existing ROS 2 Humble software stack. The GitHub
repository and recommended local workspace directory are now named
``robofleet_ws``. Some inherited runtime/configuration identifiers retain the
``roboflock`` name for compatibility.

Workspace build
---------------

.. code-block:: bash

   source /opt/ros/humble/setup.bash
   cd ~/robofleet_ws
   rosdep install --from-path src --rosdistro humble -y
   colcon build --symlink-install --executor sequential
   source install/setup.bash

Use our current development branch. During the beacon-following work,
the integration branch is ``beacon-follow``.

Bringup modes
-------------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Argument
     - Purpose
   * - ``hardware:=true``
     - Starts real robot sensor and hardware drivers.
   * - ``hardware:=false``
     - Starts navigation processes without the physical hardware drivers.
   * - ``sim:=true``
     - Runs the hardware-free integration path with simulated robot/sensors.
   * - ``slam:=true``
     - SLAM Toolbox owns ``map -> odom``.
   * - ``slam:=false``
     - GPS/global EKF owns ``map -> odom``; required for follow/home modes.

Example
-------

.. code-block:: bash

   ros2 launch bring_up bringup.launch.py follow:=true slam:=false

.. warning::

   A successful build does **not** prove GPS heading, TF ownership, motor
   safety, or sensor mounting are correct on the physical robot.
