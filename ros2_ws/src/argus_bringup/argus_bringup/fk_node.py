
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from argus_bringup.forward_kinematics import forward_kinematics
from geometry_msgs.msg import PointStamped


class ForwardKinematicsNode(Node):

    def __init__(self):
        super().__init__("forward_kinematics_node")

        # Subscribe to the robot's joint states
        self.subscription = self.create_subscription(
            JointState,
            "/joint_states",
            self.joint_state_callback,
            10
        )
        self.position_publisher = self.create_publisher(
            PointStamped,
            "/argus/tool_position",
            10
        )

        self.get_logger().info("ARGUS FK node started")


    def joint_state_callback(self, msg):
        # Associate each joint name with its angle
        joints = dict(zip(msg.name, msg.position))

        required_joints = [
            "base_rotation_joint",
            "shoulder_joint",
            "elbow_joint",
            "wrist_joint",
        ]

        # Ensure all four joint positions are available
        if not all(name in joints for name in required_joints):
            self.get_logger().warning("Missing required joint positions")
            return

        theta1 = joints["base_rotation_joint"]
        theta2 = joints["shoulder_joint"]
        theta3 = joints["elbow_joint"]
        theta4 = joints["wrist_joint"]

        # Calculate the tool-tip position
        x, y, z = forward_kinematics(
            theta1, theta2, theta3, theta4
        )

        # Create a stamped position message
        position_msg = PointStamped()

        # Identify the coordinate frame
        position_msg.header.frame_id = "base_link"

        # Timestamp the calculation
        position_msg.header.stamp = self.get_clock().now().to_msg()

        # Store the calculated coordinates
        position_msg.point.x = x
        position_msg.point.y = y
        position_msg.point.z = z

        # Publish the tool-tip position
        self.position_publisher.publish(position_msg)


        self.get_logger().info(
            f"Tool position: x={x:.4f}, y={y:.4f}, z={z:.4f} m"
        )



def main(args=None):
    # Initialize ROS 2
    rclpy.init(args=args)

    # Create our node
    node = ForwardKinematicsNode()

    try:
        # Keep the node running and process incoming messages
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        # Clean up ROS 2 resources
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
