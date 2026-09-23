import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')

        self.subscription = self.create_subscription(
            Float32,
            'front_distance',
            self.distance_callback,
            10
        )

        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.safe_distance = 0.5

        self.get_logger().info(
            'Controller node started. Sub: /front_distance, Pub: /cmd_vel'
        )

    def distance_callback(self, msg: Float32):
        distance = msg.data
        cmd = Twist()

        if distance > self.safe_distance:
            cmd.linear.x = 0.3
            cmd.angular.z = 0.0
            status = 'MOVING FORWARD'
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.6
            status = 'TURNING (OBSTACLE AHEAD)'

        self.cmd_pub.publish(cmd)
        self.get_logger().info(
            f'Distance: {distance:.2f} m -> {status}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
