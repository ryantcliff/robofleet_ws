Navigation & Localization
=========================

We use two localization modes. Mapping builds a SLAM map; follow/home mode
uses GPS-aligned localization so a latitude and longitude can become a
Nav2 target. Implemented software is not a verified outdoor GPS setup.

Transform ownership
-------------------

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - Mode
     - ``map -> odom`` publisher
     - ``odom -> base_link`` publisher
   * - ``slam:=true``
     - SLAM Toolbox
     - Local EKF
   * - ``slam:=false``
     - GPS/global EKF
     - Local EKF

RF2O publishes laser odometry on ``/odom_rf2o``. The local EKF combines
laser odometry with IMU data and publishes ``/odometry/local``. Use the
repository's RF2O launch/configuration: the upstream RF2O launcher may
also broadcast ``odom -> base_link`` and must not be run concurrently
with the local EKF's TF broadcaster.

Nav2's controller, navigator and velocity smoother use ``/odometry/local``.
In GPS mode, ``navsat_transform_node`` uses its own YAML configuration
section; the global EKF combines GPS position with heading and local
motion. Mapping mode intentionally omits the global GPS EKF and navsat
transform.

``enable_mapping:=false`` disables the selected map source, **not** the
localization mode. ``hardware:=false`` excludes EKFs and drivers unless
``sim:=true`` selects the fake-sensor localization path.

GPS and heading commissioning
-----------------------------

The old MPU-6050 has no magnetometer, so its legacy driver does not
supply a trustworthy absolute yaw. The code includes a BNO085 driver,
but real hardware mounting and calibration have not been verified.

Before real GPS follow mode, measure and publish the GPS antenna's
``base_link -> gps`` transform; verify mounted IMU axes, ENU yaw,
magnetic declination and ``yaw_offset``; and check the saved map's
datum/orientation. A saved arbitrary SLAM map is not automatically
georeferenced, and the automatic datum is not saved between runs.

Nav2 tuning: current software
-----------------------------

``src/bring_up/config/nav2_params.yaml`` selects Regulated Pure Pursuit,
not MPPI (the inherited testing found MPPI too expensive for the Orin
Nano). Current settings include:

* ``controller_frequency: 10.0`` Hz;
* ``desired_linear_vel: 1.2`` m/s;
* velocity-smoother linear acceleration ``0.5`` m/s² and deceleration
  ``-1.5`` m/s².

These are **configured targets**, not verified measured stopping
distances or actual speed. The settings prioritize walking-beacon
tracking; steady-state following lag remains to be characterized
on real hardware. Inspect the configuration file before tuning.

Refer to :doc:`../tutorials/navigation_debugging` for a no-hardware
startup check and :doc:`../tutorials/simulation` for synthetic tests.
