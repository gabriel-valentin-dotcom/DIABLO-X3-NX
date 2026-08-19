import math
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Bool, String


class RealSenseSafetyNode(Node):
    def __init__(self):
        super().__init__('realsense_safety_node')

        self.declare_parameter('depth_topic', '/camera/camera/depth/image_rect_raw')
        self.declare_parameter('stop_distance_m', 0.50)
        self.declare_parameter('slow_distance_m', 1.00)

        self.depth_topic = self.get_parameter('depth_topic').value
        self.stop_distance_m = float(self.get_parameter('stop_distance_m').value)
        self.slow_distance_m = float(self.get_parameter('slow_distance_m').value)

        self.state_pub = self.create_publisher(String, '/safety_state', 10)
        self.stop_pub = self.create_publisher(Bool, '/safety_stop', 10)

        self.sub = self.create_subscription(
            Image,
            self.depth_topic,
            self.depth_callback,
            10
        )

        self.get_logger().info(f'Safety Layer listening: {self.depth_topic}')

    def depth_callback(self, msg: Image):
        if msg.encoding != '16UC1':
            self.get_logger().warn(f'Unsupported depth encoding: {msg.encoding}')
            return

        depth = np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.width)

        h, w = depth.shape

        # Center safety window
        y1 = int(h * 0.40)
        y2 = int(h * 0.70)
        x1 = int(w * 0.35)
        x2 = int(w * 0.65)

        roi = depth[y1:y2, x1:x2]

        valid = roi[(roi > 0) & (roi < 10000)]

        if valid.size == 0:
            distance_m = math.inf
            state = 'NO_DEPTH'
            stop = False
        else:
            distance_m = float(np.median(valid)) / 1000.0

            if distance_m < self.stop_distance_m:
                state = f'STOP {distance_m:.2f}m'
                stop = True
            elif distance_m < self.slow_distance_m:
                state = f'SLOW {distance_m:.2f}m'
                stop = False
            else:
                state = f'CLEAR {distance_m:.2f}m'
                stop = False

        self.state_pub.publish(String(data=state))
        self.stop_pub.publish(Bool(data=stop))

        self.get_logger().info(state)


def main(args=None):
    rclpy.init(args=args)
    node = RealSenseSafetyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
