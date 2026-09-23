import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random


class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')

        self.publisher_ = self.create_publisher(Float32, 'front_distance', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info(
            'Sensor node started, publishing /front_distance'
        )

    def timer_callback(self):
        msg = Float32()
        msg.data = random.uniform(0.1, 2.0)

        self.publisher_.publish(msg)
        self.get_logger().info(f'Front distance: {msg.data:.2f} m')


def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
