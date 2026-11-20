"""Pin the URDF frames that the real robot and the simulator depend on.

Run with the workspace sourced:
    python3 -m pytest src/urdf_description/test/test_urdf_frames.py
"""

import os
import xml.etree.ElementTree as ET

import numpy as np
import pytest

xacro = pytest.importorskip('xacro')
get_share = pytest.importorskip('ament_index_python.packages').get_package_share_directory

ROBOT = None


def robot():
    global ROBOT
    if ROBOT is None:
        path = os.path.join(get_share('urdf_description'), 'urdf', 'URDF.xacro')
        ROBOT = ET.fromstring(xacro.process_file(path).toxml())
    return ROBOT


def rpy_matrix(roll, pitch, yaw):
    cr, sr, cp, sp, cy, sy = (np.cos(roll), np.sin(roll), np.cos(pitch),
                              np.sin(pitch), np.cos(yaw), np.sin(yaw))
    return np.array([
        [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
        [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
        [-sp, cp * sr, cp * cr]])


def joints():
    out = {}
    for joint in robot().findall('joint'):
        origin = joint.find('origin')
        xyz = np.array([float(v) for v in origin.get('xyz', '0 0 0').split()])
        rot = rpy_matrix(*[float(v) for v in origin.get('rpy', '0 0 0').split()])
        axis = joint.find('axis')
        axis = np.array([float(v) for v in axis.get('xyz').split()]) if axis is not None else None
        out[joint.find('child').get('link')] = (
            joint.find('parent').get('link'), xyz, rot, axis, joint.get('name'))
    return out


def pose(link, table):
    """Position and rotation of `link` in base_link."""
    if link not in table:
        return np.zeros(3), np.eye(3)
    parent, xyz, rot, _, _ = table[link]
    p_pos, p_rot = pose(parent, table)
    return p_pos + p_rot @ xyz, p_rot @ rot


def test_sensor_frames_match_the_real_robot():
    # These are what navsat_transform, the lidar driver and Nav2 consume on
    # the real robot. Changing them changes real-world behaviour.
    table = joints()
    gps_pos, gps_rot = pose('gps', table)
    np.testing.assert_allclose(gps_pos, [0.16, 0.0, 0.461], atol=1e-6)
    np.testing.assert_allclose(gps_rot, np.eye(3), atol=1e-9)
    lidar_pos, lidar_rot = pose('lidar_link', table)
    np.testing.assert_allclose(lidar_pos, [0.0, 0.0, 0.949], atol=1e-3)
    np.testing.assert_allclose(lidar_rot, np.eye(3), atol=1e-9)


def test_wheels_roll_forward_along_x():
    # REP-103: x forward, y left. A positive spin on every wheel joint must
    # push the robot towards +x, or the Gazebo diff drive goes sideways.
    table = joints()
    for name, side in [('lf', 1), ('lr', 1), ('rf', -1), ('rr', -1)]:
        child = next(c for c, j in table.items() if j[4] == f'{name}_wheel_to_coupling')
        pos, rot = pose(child, table)
        assert np.sign(pos[1]) == side, f'{name} wheel is on the wrong side: {pos}'
        axis = rot @ table[child][3]
        ground_contact = np.cross(axis, [0, 0, -1])  # contact-point velocity
        assert ground_contact[0] < -0.99, f'{name} wheel does not drive +x: axis {axis}'
