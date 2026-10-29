import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StatusPublisher(Node):
    def __init__(self):
        super().__init__('argus_status_publisher')

        self.publisher = self.create_publisher(
            String,
            '/argus/status',
            10
        )

        self.timer = self.create_timer(1.0, self.publish_status)

    def publish_status(self):
        message = String()
        message.data = 'ARGUS system online'

        self.publisher.publish(message)
        self.get_logger().info(f'Published: {message.data}')


def main(args=None):
    rclpy.init(args=args)
    node = StatusPublisher()

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
