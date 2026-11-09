"""Tests for the ROS 2 inverse-kinematics node."""
from argus_bringup.ik_node import InverseKinematicsNode

from geometry_msgs.msg import PointStamped

import rclpy


def test_rejected_target_does_not_skip_initialization():
    """Confirm rejected targets leave startup initialization pending."""
    initialized_rclpy = not rclpy.ok()
    if initialized_rclpy:
        rclpy.init()

    node = InverseKinematicsNode()
    try:
        target = PointStamped()
        target.header.frame_id = 'base_link'
        target.point.x = 1.0
        target.point.z = 0.3

        node.target_callback(target)

        assert not node.initialized
    finally:
        node.destroy_node()
        if initialized_rclpy and rclpy.ok():
            rclpy.shutdown()
