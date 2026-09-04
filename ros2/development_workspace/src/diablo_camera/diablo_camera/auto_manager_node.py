#!/usr/bin/env python3

import subprocess
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class AutoManager(Node):

    def __init__(self):
        super().__init__('auto_manager_node')

        self.sub = self.create_subscription(
            String,
            '/system_command',
            self.cb,
            10
        )

        self.get_logger().info('AUTO Manager V2 aktiv: no mode publisher')

    def send_system(self, cmd):
        subprocess.call(
            f"ros2 topic pub --once /system_command std_msgs/msg/String \"{{data: '{cmd}'}}\"",
            shell=True
        )

    def auto_on(self):
        self.send_system('CAM_ON')
        self.get_logger().info('AUTO ON helper: CAM_ON sent')

    def auto_off(self):
        self.send_system('FOLLOW_OFF')
        self.get_logger().info('AUTO OFF helper: FOLLOW_OFF sent, camera unchanged unless CAM_OFF/STOP')

    def cb(self, msg):
        cmd = msg.data.strip().upper()

        if cmd == 'AUTO_ON':
            self.auto_on()

        elif cmd == 'AUTO_OFF':
            self.auto_off()


def main():
    rclpy.init()
    node = AutoManager()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
