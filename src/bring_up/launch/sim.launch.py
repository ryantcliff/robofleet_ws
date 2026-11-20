"""Hardware-free robot: Gazebo + the real SLAM and Nav2 launch files.

    ros2 launch bring_up sim.launch.py                    # Gazebo + SLAM + Nav2
    ros2 launch bring_up sim.launch.py nav:=false         # just drive it around
    ros2 launch bring_up sim.launch.py foxglove:=true     # view it in a browser

Over SSH, prefer `scripts/sim.sh`: it picks a free ROS domain and Foxglove
port so several people can simulate on the Jetson at once.

Nothing here talks to motors or sensors. Gazebo publishes what the real
drivers and EKF would: /scan, /odometry/local and odom->base_link. SLAM
adds map->odom and Nav2 drives /cmd_vel.
"""

from ament_index_python.packages import (get_package_share_directory,
                                         PackageNotFoundError)
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            OpaqueFunction, TimerAction)
from launch.conditions import IfCondition
from launch.launch_description_sources import (
    AnyLaunchDescriptionSource, PythonLaunchDescriptionSource)
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def share(package, *path):
    return PathJoinSubstitution([FindPackageShare(package), *path])


def foxglove(context):
    if LaunchConfiguration('foxglove').perform(context).lower() not in ('1', 'true'):
        return []
    try:
        fox = get_package_share_directory('foxglove_bridge')
    except PackageNotFoundError:
        raise RuntimeError('foxglove:=true but foxglove_bridge is not installed. '
                           'Run: sudo apt install ros-humble-foxglove-bridge')
    return [IncludeLaunchDescription(
        AnyLaunchDescriptionSource(f'{fox}/launch/foxglove_bridge_launch.xml'),
        launch_arguments={
            'port': LaunchConfiguration('foxglove_port'),
            # Localhost only: reach it through `ssh -L`, not the open network.
            'address': '127.0.0.1',
            'use_sim_time': 'true',
        }.items())]


def generate_launch_description():
    nav = IfCondition(LaunchConfiguration('nav'))
    return LaunchDescription([
        DeclareLaunchArgument('nav', default_value='true',
                              description='Run slam_toolbox and Nav2 on the simulated robot'),
        DeclareLaunchArgument('foxglove', default_value='false',
                              description='Start foxglove_bridge on 127.0.0.1:<foxglove_port>'),
        DeclareLaunchArgument('foxglove_port', default_value='8765'),
        DeclareLaunchArgument('world', default_value='test_yard.sdf'),
        DeclareLaunchArgument('headless', default_value='auto'),
        DeclareLaunchArgument('rviz', default_value='false'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(share('urdf_description', 'launch', 'gazebo.launch.py')),
            launch_arguments={
                'world': LaunchConfiguration('world'),
                'headless': LaunchConfiguration('headless'),
                'rviz': LaunchConfiguration('rviz'),
            }.items()),

        # Give Gazebo time to spawn the robot and start /clock before the
        # sim-time nodes start waiting on TF.
        TimerAction(period=8.0, actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(share('bring_up', 'launch', 'slam.launch.py')),
                launch_arguments={'use_sim_time': 'true'}.items(),
                condition=nav),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(share('bring_up', 'launch', 'nav2.launch.py')),
                launch_arguments={'use_sim_time': 'true', 'autostart': 'true'}.items(),
                condition=nav),
        ]),

        OpaqueFunction(function=foxglove),
    ])
