
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StatusSubscriber(Node):
    def __init__(self):
        super().__init__('argus_status_subscriber')

        self.subscription = self.create_subscription(
            String,
            '/argus/status',
            self.status_callback,
            10
        )

    def status_callback(self, message):
        self.get_logger().info(
            f'Received: {message.data}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = StatusSubscriber()

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
