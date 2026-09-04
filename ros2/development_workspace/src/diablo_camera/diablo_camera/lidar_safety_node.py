#!/usr/bin/env python3
import math
import statistics
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, String


class LidarSafetyNode(Node):

    def __init__(self):
        super().__init__('lidar_safety_node')

        self.min_valid_m = 0.18
        self.max_valid_m = 3.5

        self.any_stop_m = 0.30
        self.any_stop_min_points = 3
        self.any_near_stop_m = 0.45
        self.front_stop_m = 0.55
        self.side_stop_m = 0.50
        self.back_stop_m = 0.35

        # Diablo build convention: camera/front is +/-180 deg, rear is 0 deg.
        self.front_sector_a_deg = (155.0, 180.0)
        self.front_sector_b_deg = (-180.0, -155.0)
        self.front_left_sector_deg = (-155.0, -125.0)
        self.front_right_sector_deg = (125.0, 155.0)
        self.left_sector_deg = (-115.0, -65.0)
        self.right_sector_deg = (65.0, 115.0)
        self.back_sector_deg = (-25.0, 25.0)

        self.min_points_per_zone = 3

        self.safe_pub = self.create_publisher(Bool, '/diablo/safety/lidar_safe', 10)
        self.status_pub = self.create_publisher(String, '/diablo/safety/lidar_status', 10)
        self.safe_filtered_pub = self.create_publisher(Bool, '/diablo/safety/lidar_safe_filtered', 10)
        self.status_filtered_pub = self.create_publisher(String, '/diablo/safety/lidar_status_filtered', 10)
        scan_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.BEST_EFFORT,
        )
        self.sub = self.create_subscription(LaserScan, '/scan', self.on_scan, scan_qos)
        self.last_scan_time = 0.0
        self.last_safe = False
        self.last_status = 'LIDAR_STALE age=inf'
        self.scan_timeout_s = 0.8
        self.timer = self.create_timer(0.25, self.publish_status)

        self.get_logger().info('LiDAR Safety V3 aktiv: 4 zones + median')

    def in_sector(self, angle_deg, sector):
        return sector[0] <= angle_deg <= sector[1]

    def median_or_none(self, values):
        if len(values) < self.min_points_per_zone:
            return None
        return statistics.median(values)

    def fmt(self, value):
        if value is None:
            return 'none'
        return f'{value:.2f}'

    def on_scan(self, msg):
        self.last_scan_time = time.monotonic()
        front_vals = []
        front_left_vals = []
        front_right_vals = []
        left_vals = []
        right_vals = []
        back_vals = []
        all_vals = []
        any_stop_vals = []

        for i, r in enumerate(msg.ranges):
            if not math.isfinite(r):
                continue
            if r < self.min_valid_m or r > self.max_valid_m:
                continue

            angle = msg.angle_min + i * msg.angle_increment
            angle_deg = math.degrees(angle)

            all_vals.append(r)
            if r < self.any_stop_m:
                any_stop_vals.append(r)

            if (
                self.in_sector(angle_deg, self.front_sector_a_deg) or
                self.in_sector(angle_deg, self.front_sector_b_deg)
            ):
                front_vals.append(r)

            if self.in_sector(angle_deg, self.front_left_sector_deg):
                front_left_vals.append(r)

            if self.in_sector(angle_deg, self.front_right_sector_deg):
                front_right_vals.append(r)

            if self.in_sector(angle_deg, self.left_sector_deg):
                left_vals.append(r)

            if self.in_sector(angle_deg, self.right_sector_deg):
                right_vals.append(r)

            if self.in_sector(angle_deg, self.back_sector_deg):
                back_vals.append(r)

        front = self.median_or_none(front_vals)
        front_left = self.median_or_none(front_left_vals)
        front_right = self.median_or_none(front_right_vals)
        left = self.median_or_none(left_vals)
        right = self.median_or_none(right_vals)
        back = self.median_or_none(back_vals)

        any_near = min(all_vals) if all_vals else None
        any_stop = self.median_or_none(any_stop_vals)

        safe = True
        reason = 'SAFE'

        if any_near is None:
            safe = False
            reason = 'NO_LIDAR_DATA'
        elif front is not None and front < self.front_stop_m:
            safe = False
            reason = 'BLOCKED_FRONT'
        elif front_left is not None and front_left < self.front_stop_m:
            safe = False
            reason = 'BLOCKED_FRONT'
        elif front_right is not None and front_right < self.front_stop_m:
            safe = False
            reason = 'BLOCKED_FRONT'
        elif left is not None and left < self.side_stop_m:
            safe = False
            reason = 'BLOCKED_LEFT'
        elif right is not None and right < self.side_stop_m:
            safe = False
            reason = 'BLOCKED_RIGHT'
        elif back is not None and back < self.back_stop_m:
            safe = False
            reason = 'BLOCKED_BACK'
        elif (
            len(any_stop_vals) >= self.any_stop_min_points and
            any_stop is not None and
            any_stop < self.any_stop_m
        ):
            # Very short-range returns outside named sectors can be stable
            # self-echoes from DIABLO's body. Keep them diagnostic; hard stops
            # are owned by the named front/side/back sectors above.
            reason = 'SAFE_ANY_NEAR'

        text = (
            f'{reason} '
            f'front={self.fmt(front)}m '
            f'fl={self.fmt(front_left)}m '
            f'fr={self.fmt(front_right)}m '
            f'left={self.fmt(left)}m '
            f'right={self.fmt(right)}m '
            f'back={self.fmt(back)}m '
            f'any={self.fmt(any_near)}m '
            f'any_stop={self.fmt(any_stop)}m '
            f'pts=F{len(front_vals)} '
            f'FL{len(front_left_vals)} '
            f'FR{len(front_right_vals)} '
            f'L{len(left_vals)} '
            f'R{len(right_vals)} '
            f'B{len(back_vals)} '
            f'ANY{len(any_stop_vals)}'
        )

        self.last_safe = safe
        self.last_status = text

    def publish_status(self):
        now = time.monotonic()
        age = now - self.last_scan_time if self.last_scan_time > 0.0 else float('inf')

        if age > self.scan_timeout_s:
            safe = False
            age_text = 'inf' if not math.isfinite(age) else f'{age:.2f}'
            text = f'LIDAR_STALE age={age_text}s'
        else:
            safe = self.last_safe
            text = self.last_status

        self.safe_pub.publish(Bool(data=safe))
        self.status_pub.publish(String(data=text))
        self.safe_filtered_pub.publish(Bool(data=safe))
        self.status_filtered_pub.publish(String(data=text))


def main():
    rclpy.init()
    node = LidarSafetyNode()

    try:
        rclpy.spin(node)
    finally:
        node.safe_pub.publish(Bool(data=False))
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
