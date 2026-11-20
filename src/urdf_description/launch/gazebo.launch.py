"""Spawn the robot in Gazebo Fortress (ROS 2 Humble) and bridge it to ROS.

    ros2 launch urdf_description gazebo.launch.py                 # headless if no display
    ros2 launch urdf_description gazebo.launch.py headless:=false rviz:=true

ROS topics afterwards: /cmd_vel (drive it), /odometry/local, /tf, /scan,
/joint_states, /clock, /robot_description. For SLAM + Nav2 on top, use
`ros2 launch bring_up sim.launch.py`, or `scripts/sim.sh` over SSH.

Needs: sudo apt install ros-humble-ros-gz
"""

import getpass
import os

from ament_index_python.packages import (get_package_share_directory,
                                         PackageNotFoundError)
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            OpaqueFunction, SetEnvironmentVariable)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro

INSTALL_HINT = 'Gazebo is not installed. Run: sudo apt install ros-humble-ros-gz'


def truthy(value):
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def launch_setup(context):
    try:
        gz_share = get_package_share_directory('ros_gz_sim')
    except PackageNotFoundError:
        raise RuntimeError(INSTALL_HINT)

    share = get_package_share_directory('urdf_description')
    robot_urdf = xacro.process_file(
        os.path.join(share, 'urdf', 'URDF.xacro')).toxml()

    headless = LaunchConfiguration('headless').perform(context)
    headless = (not os.environ.get('DISPLAY')) if headless == 'auto' else truthy(headless)
    world = LaunchConfiguration('world').perform(context)
    if not os.path.isabs(world):
        world = os.path.join(share, 'worlds', world)

    # -s: server only (no window). --headless-rendering lets the gpu_lidar
    # render without a display (EGL), which is what SSH sessions need.
    gz_args = f'-r -s --headless-rendering {world}' if headless else f'-r {world}'

    sim_time = {'use_sim_time': True}
    actions = [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gz_share, 'launch', 'gz_sim.launch.py')),
            launch_arguments={'gz_args': gz_args}.items()),

        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_urdf}, sim_time],
             output='screen'),

        Node(package='ros_gz_sim', executable='create', output='screen',
             arguments=['-name', 'roboflock', '-topic', 'robot_description',
                        '-x', LaunchConfiguration('x').perform(context),
                        '-y', LaunchConfiguration('y').perform(context),
                        '-z', '0.25',
                        '-Y', LaunchConfiguration('yaw').perform(context)]),

        # ROS <-> Gazebo. "]" = ROS to Gazebo, "[" = Gazebo to ROS.
        Node(package='ros_gz_bridge', executable='parameter_bridge', output='screen',
             arguments=[
                 '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
                 '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
                 '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
                 '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
                 '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
                 '/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model',
             ],
             # Nav2 (nav2_params.yaml) reads odometry from /odometry/local,
             # which the EKF publishes on the real robot.
             remappings=[('/odom', '/odometry/local')],
             parameters=[sim_time]),
    ]

    if truthy(LaunchConfiguration('rviz').perform(context)):
        if headless:
            print('[gazebo.launch] rviz:=true ignored: no display (headless). '
                  'Use foxglove:=true with an SSH tunnel instead.')
        else:
            actions.append(Node(
                package='rviz2', executable='rviz2', output='screen',
                arguments=['-d', os.path.join(share, 'config', 'gazebo.rviz')],
                parameters=[sim_time]))
    return actions


def generate_launch_description():
    # Gazebo's own transport is not split by ROS_DOMAIN_ID. A per-user,
    # per-domain partition keeps two people's simulations apart.
    partition = os.environ.get('IGN_PARTITION') or '{}_{}'.format(
        getpass.getuser(), os.environ.get('ROS_DOMAIN_ID', '0'))
    return LaunchDescription([
        DeclareLaunchArgument(
            'world', default_value='test_yard.sdf',
            description='SDF file in urdf_description/worlds, or an absolute path'),
        DeclareLaunchArgument(
            'headless', default_value='auto',
            description='true: no Gazebo window. auto: headless when $DISPLAY is unset'),
        DeclareLaunchArgument('rviz', default_value='false'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('yaw', default_value='0.0'),
        SetEnvironmentVariable('IGN_PARTITION', partition),
        OpaqueFunction(function=launch_setup),
    ])
