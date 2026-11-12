"""ROS 2 node for interpolated ARGUS joint motion."""

import math
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool

from argus_bringup.trajectory import (
    calculate_duration,
    trajectory_at_time,
    trajectory_complete,
)


JOINT_NAMES = [
    'base_rotation_joint',
    'shoulder_joint',
    'elbow_joint',
    'wrist_joint',
]

MAX_VELOCITIES = (0.5, 0.5, 0.5, 0.5)


class TrajectoryNode(Node):
    """Convert joint targets into time-based motion."""

    def __init__(self):
        """Initialize trajectory state and ROS interfaces."""
        super().__init__('trajectory_node')

        self.current = (0.0, 0.0, 0.0, 0.0)
        self.start = self.current
        self.target = self.current

        self.duration = 0.0
        self.start_time = time.monotonic()

        self.command_subscriber = self.create_subscription(
            JointState,
            '/argus/joint_commands',
            self.command_callback,
            10,
        )

        self.state_publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10,
        )

        self.status_publisher = self.create_publisher(
            Bool,
            '/argus/trajectory_complete',
            10,
        )

        self.timer = self.create_timer(
            1.0 / 30.0,
            self.update,
        )

        self.get_logger().info('ARGUS trajectory node ready')

    def position_at(self, now):
        """Return the interpolated position at the given time."""
        elapsed = max(0.0, now - self.start_time)

        return trajectory_at_time(
            self.start,
            self.target,
            elapsed,
            self.duration,
        )

    def command_callback(self, msg):
        """Accept a valid joint target and begin interpolation."""
        if (
            len(msg.name) != len(JOINT_NAMES)
            or set(msg.name) != set(JOINT_NAMES)
            or len(msg.position) != len(JOINT_NAMES)
        ):
            self.get_logger().warn(
                'Rejected command: invalid joint configuration'
            )
            return

        positions = dict(zip(msg.name, msg.position))

        target = tuple(
            positions[name] for name in JOINT_NAMES
        )

        if not all(math.isfinite(angle) for angle in target):
            self.get_logger().warn(
                'Rejected command: non-finite joint angle'
            )
            return

        now = time.monotonic()

        # Continue from the current interpolated position
        # if a new target arrives during an existing movement.
        self.current = self.position_at(now)
        self.start = self.current
        self.target = target

        self.duration = 1.5 * calculate_duration(
            self.start,
            self.target,
            MAX_VELOCITIES,
        )

        self.start_time = now

        self.get_logger().info(
            f'New trajectory: {self.duration:.2f} seconds'
        )

    def update(self):
        """Publish the current interpolated joint configuration."""
        now = time.monotonic()
        self.current = self.position_at(now)

        state = JointState()
        state.header.stamp = self.get_clock().now().to_msg()
        state.header.frame_id = 'base_link'

        state.name = list(JOINT_NAMES)
        state.position = list(self.current)

        self.state_publisher.publish(state)
        elapsed = now - self.start_time

        complete = Bool()
        complete.data = trajectory_complete(
            elapsed,
            self.duration,
        )

        self.status_publisher.publish(complete)


def main(args=None):
    """Initialize and run the trajectory node."""
    rclpy.init(args=args)
    node = TrajectoryNode()

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
