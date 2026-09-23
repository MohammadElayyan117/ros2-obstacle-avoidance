import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')

        self.distance = None
        self.last_cmd = None

        self.create_subscription(
            Float32,
            'front_distance',
            self.distance_callback,
            10
        )

        self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_callback,
            10
        )

        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info(
            'Monitor node started. Watching /front_distance and /cmd_vel'
        )

    def distance_callback(self, msg: Float32):
        self.distance = msg.data

    def cmd_callback(self, msg: Twist):
        self.last_cmd = msg

    def timer_callback(self):
        if self.distance is None or self.last_cmd is None:
            return

        moving_state = 'STOPPED'

        if abs(self.last_cmd.linear.x) > 1e-3:
            moving_state = 'MOVING FORWARD'
        elif abs(self.last_cmd.angular.z) > 1e-3:
            moving_state = 'TURNING'

        self.get_logger().info(
            f'[MONITOR] Distance: {self.distance:.2f} m | '
            f'State: {moving_state}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = MonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
