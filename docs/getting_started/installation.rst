Installation & Build
====================

We are still on ROS 2 Humble. The GitHub repo and our workspace folder are now
called ``robofleet_ws``. A few names inside the code still say ``roboflock``
(config files, device rules, namespaces). We left those alone on purpose,
because renaming them would break things that work.

Building the workspace
----------------------

.. code-block:: bash

   source /opt/ros/humble/setup.bash
   cd ~/robofleet_ws
   rosdep install --from-path src --rosdistro humble -y
   colcon build --symlink-install --executor sequential
   source install/setup.bash

We work from ``main``. ``beacon-follow`` is an older integration branch.

Bringup options
---------------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Argument
     - What it does
   * - ``hardware:=true``
     - Starts the real sensor and hardware drivers.
   * - ``hardware:=false``
     - Starts navigation without the hardware drivers.
   * - ``sim:=true``
     - Runs everything with a simulated robot and sensors, no hardware.
   * - ``slam:=true``
     - SLAM Toolbox owns the ``map -> odom`` transform.
   * - ``slam:=false``
     - The GPS / global EKF owns ``map -> odom``. Follow and home modes need this.

Example
-------

.. code-block:: bash

   ros2 launch bring_up bringup.launch.py follow:=true slam:=false

.. warning::

   Building successfully does not tell you the GPS heading, the transforms, the
   motor safety or the sensor mounting are right on the real robot.

Joystick drive service
----------------------

The robot has a systemd service, ``roboflock-drive.service``, that starts the
joystick drive stack (``bring_up.sh``) when the Jetson boots. The unit file is
in ``src/bring_up/systemd``. We currently have it **turned off** on the robot.

When it runs, ``diff_drive_controller`` connects to the four motor controllers
by itself as soon as they show up on USB. The e-stop starts engaged. Pressing
**Options** on the PS4 controller arms the motors, and **Cross** stops them. So
if the motor battery is connected and the service is running, one button press
makes the robot drive.

.. code-block:: bash

   sudo systemctl enable --now roboflock-drive    # start now and on every boot
   sudo systemctl disable --now roboflock-drive   # stop now and on every boot
   journalctl -u roboflock-drive -f               # watch what it is doing
