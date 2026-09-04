#!/usr/bin/env python3

import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from motion_msgs.msg import LegMotors


class MotorStallProtectNode(Node):

    def __init__(self):
        super().__init__('motor_stall_protect_node')

        self.last_cmd = 'HOLD_NO_MOVE'
        self.last_lidar_status = 'WAIT'

        self.stall_since = None
        self.last_hold_time = 0.0

        self.iq_limit = 3.0
        self.vel_limit = 0.05
        self.stall_time = 0.4
        self.hold_repeat_time = 0.2

        self.create_subscription(
            String,
            '/diablo_motion_request',
            self.on_cmd,
            10
        )

        self.create_subscription(
            String,
            '/diablo/safety/lidar_status',
            self.on_lidar,
            10
        )

        self.create_subscription(
            LegMotors,
            '/diablo/sensor/Motors',
            self.on_motors,
            10
        )

        self.status_pub = self.create_publisher(
            String,
            '/diablo/safety/motor_stall_status',
            10
        )

        self.motion_pub = self.create_publisher(
            String,
            '/diablo_motion_request',
            10
        )

        self.feedback_pub = self.create_publisher(
            String,
            '/diablo_feedback',
            10
        )

        self.get_logger().info(
            'MOTOR_STALL_PROTECT_V1_1_STABLE aktiv'
        )

    def on_cmd(self, msg):
        self.last_cmd = msg.data

    def on_lidar(self, msg):
        self.last_lidar_status = msg.data

    def lidar_blocked(self):
        return self.last_lidar_status in [
            'NOT_SAFE',
            'FRONT_BLOCKED',
            'BLOCKED'
        ]

    def send_hold(self):
        now = time.time()

        if now - self.last_hold_time >= self.hold_repeat_time:
            self.motion_pub.publish(
                String(data='HOLD_NO_MOVE')
            )

            self.feedback_pub.publish(
                String(data='MOTOR_STALL_PROTECT')
            )

            self.last_hold_time = now

    def on_motors(self, m):

        driving = self.last_cmd in [
            'MOVE_UP',
            'MOVE_DOWN',
            'TURN_LEFT',
            'TURN_RIGHT',
            'FORWARD_SLOW',
            'BACKWARD_SLOW',
            'TURN_LEFT_SLOW',
            'TURN_RIGHT_SLOW'
        ]

        wheel_stopped = (
            abs(m.left_wheel_vel) < self.vel_limit and
            abs(m.right_wheel_vel) < self.vel_limit
        )

        wheel_current_high = (
            abs(m.left_wheel_iq) > self.iq_limit or
            abs(m.right_wheel_iq) > self.iq_limit
        )

        now = time.time()

        if driving and wheel_stopped and wheel_current_high:

            if self.stall_since is None:
                self.stall_since = now

            if now - self.stall_since >= self.stall_time:

                if self.lidar_blocked():

                    self.status_pub.publish(
                        String(
                            data='STALL_DETECTED_LIDAR_CONFIRMED_HOLD'
                        )
                    )

                    self.send_hold()
                    return

                else:

                    self.status_pub.publish(
                        String(
                            data='STALL_POSSIBLE_LIDAR_NOT_CONFIRMED'
                        )
                    )

                    return

        else:
            self.stall_since = None

        self.status_pub.publish(
            String(data='OK')
        )


def main(args=None):
    rclpy.init(args=args)

    node = MotorStallProtectNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
