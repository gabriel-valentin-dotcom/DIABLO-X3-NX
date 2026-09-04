#!/usr/bin/env python3

import math
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import (
    HistoryPolicy,
    QoSProfile,
    ReliabilityPolicy,
)
from std_msgs.msg import String, Bool
from sensor_msgs.msg import LaserScan


class SafetyBubbleNode(Node):

    def __init__(self):
        super().__init__('safety_bubble_node')

        self.stop_m = 0.35
        self.slow_m = 0.60
        self.warn_m = 0.90
        self.self_filter_m = 0.18

        self.last_scan_time = 0.0
        self.scan_timeout = 1.0
        self.scan_recovery_interval = 5.0
        self.last_scan_recovery_time = 0.0
        self.scan_count = 0
        self.scan_subscriptions = []

        self.front = 9.9
        self.front_left = 9.9
        self.front_right = 9.9
        self.left = 9.9
        self.right = 9.9
        self.back = 9.9

        self.pub_ok = self.create_publisher(Bool, '/diablo/safety/bubble_ok', 10)
        self.pub_status = self.create_publisher(String, '/diablo/safety/bubble_status', 10)

        self.create_scan_subscriptions()
        self.timer = self.create_timer(0.2, self.tick)

        self.get_logger().info('SAFETY_BUBBLE_V1_3_SCAN_RECOVERY aktiv')

    def create_scan_subscriptions(self):
        for sub in self.scan_subscriptions:
            try:
                self.destroy_subscription(sub)
            except Exception as exc:
                self.get_logger().warn(f'BUBBLE_SCAN_SUB_DESTROY_WARN: {exc}')

        scan_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.BEST_EFFORT,
        )

        self.scan_subscriptions = [
            self.create_subscription(LaserScan, '/scan', self.on_scan, scan_qos),
        ]
        self.get_logger().info('BUBBLE_SCAN_SUBSCRIPTIONS_READY best_effort /scan')

    def on_scan(self, msg):
        self.last_scan_time = time.monotonic()
        self.scan_count += 1

        front = 9.9
        front_left = 9.9
        front_right = 9.9
        left = 9.9
        right = 9.9
        back = 9.9
        angle = msg.angle_min

        for r in msg.ranges:
            if math.isfinite(r) and self.self_filter_m <= r < 6.0:
                deg = math.degrees(angle)
                if 155 <= deg <= 180 or -180 <= deg <= -155:
                    front = min(front, r)
                elif -155 <= deg <= -125:
                    front_left = min(front_left, r)
                elif 125 <= deg <= 155:
                    front_right = min(front_right, r)
                elif -115 <= deg <= -65:
                    left = min(left, r)
                elif 65 <= deg <= 115:
                    right = min(right, r)
                elif -25 <= deg <= 25:
                    back = min(back, r)
            angle += msg.angle_increment

        self.front = front
        self.front_left = front_left
        self.front_right = front_right
        self.left = left
        self.right = right
        self.back = back

    def publish_status(self, ok_value, text):
        self.pub_ok.publish(Bool(data=ok_value))
        self.pub_status.publish(String(data=text))

    def tick(self):
        now = time.monotonic()

        if self.last_scan_time <= 0.0:
            self.recover_scan_subscription(now)
            self.publish_status(False, 'BUBBLE_NO_SCAN')
            return

        if now - self.last_scan_time > self.scan_timeout:
            self.recover_scan_subscription(now)
            self.publish_status(False, 'BUBBLE_NO_LIDAR')
            return

        nearest = min(
            self.front,
            self.front_left,
            self.front_right,
            self.left,
            self.right,
            self.back
        )

        base = (
            f'front={self.front:.2f} '
            f'front_left={self.front_left:.2f} '
            f'front_right={self.front_right:.2f} '
            f'left={self.left:.2f} '
            f'right={self.right:.2f} '
            f'back={self.back:.2f}'
        )

        if nearest < self.stop_m:
            self.publish_status(False, 'BUBBLE_STOP ' + base)
        elif nearest < self.slow_m:
            self.publish_status(True, 'BUBBLE_SLOW ' + base)
        elif nearest < self.warn_m:
            self.publish_status(True, 'BUBBLE_WARN ' + base)
        else:
            self.publish_status(True, 'BUBBLE_CLEAR ' + base)

    def recover_scan_subscription(self, now):
        if now - self.last_scan_recovery_time < self.scan_recovery_interval:
            return

        self.last_scan_recovery_time = now
        self.get_logger().warn(
            f'BUBBLE_SCAN_RECOVERY: stale/no /scan, recreating subscriptions; '
            f'scan_count={self.scan_count}'
        )
        self.create_scan_subscriptions()


def main(args=None):
    rclpy.init(args=args)
    node = SafetyBubbleNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
