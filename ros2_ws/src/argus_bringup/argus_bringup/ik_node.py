"""ROS 2 node for Cartesian inverse kinematics."""

from argus_bringup.inverse_kinematics import inverse_kinematics

from geometry_msgs.msg import PointStamped

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState


class InverseKinematicsNode(Node):
    """Convert Cartesian position targets into joint-state commands."""

    def __init__(self):
        """Create subscriptions, publishers, and startup initialization."""
        super().__init__('ik_node')

        self.target_subscriber = self.create_subscription(
            PointStamped,
            '/argus/target_position',
            self.target_callback,
            10,
        )

        self.joint_publisher = self.create_publisher(
            JointState,
            '/argus/joint_commands',
            10,
        )

        self.get_logger().info('ARGUS IK node ready')

        self.initialized = False

        self.initialization_timer = self.create_timer(
            0.5,
            self.publish_initial_pose,
        )

    def target_callback(self, msg):
        """Validate a Cartesian target and publish its IK solution."""
        # Our IK solver expects coordinates in base_link.
        if msg.header.frame_id != 'base_link':
            self.get_logger().warn(
                'Target must be expressed in base_link'
            )
            return

        x = msg.point.x
        y = msg.point.y
        z = msg.point.z

        try:
            angles = inverse_kinematics(x, y, z)

        except ValueError as error:
            self.get_logger().warn(
                f'IK target rejected: {error}'
            )
            return

        self.initialized = True
        self.initialization_timer.cancel()

        command = JointState()
        command.header.stamp = self.get_clock().now().to_msg()
        command.header.frame_id = 'base_link'

        command.name = [
            'base_rotation_joint',
            'shoulder_joint',
            'elbow_joint',
            'wrist_joint',
        ]

        command.position = list(angles)

        self.joint_publisher.publish(command)

        self.get_logger().info(
            f'IK solution published for ({x:.3f}, '
            f'{y:.3f}, {z:.3f})'
        )

    def publish_initial_pose(self):
        """Publish the upright configuration after a subscriber connects."""
        if self.initialized:
            return

        # Wait until robot_state_publisher is subscribed.
        if self.joint_publisher.get_subscription_count() == 0:
            return

        command = JointState()
        command.header.stamp = self.get_clock().now().to_msg()
        command.header.frame_id = 'base_link'

        command.name = [
            'base_rotation_joint',
            'shoulder_joint',
            'elbow_joint',
            'wrist_joint',
        ]

        command.position = [0.0, 0.0, 0.0, 0.0]

        self.joint_publisher.publish(command)

        self.initialized = True
        self.initialization_timer.cancel()

        self.get_logger().info(
            'ARGUS initialized in upright configuration'
        )


def main(args=None):
    """Initialize ROS and run the IK node."""
    rclpy.init(args=args)

    node = InverseKinematicsNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
