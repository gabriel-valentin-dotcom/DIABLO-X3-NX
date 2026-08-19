#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DiabloSystemStateNode(Node):

    def __init__(self):
        super().__init__('diablo_system_state_node')

        self.pub = self.create_publisher(
            String,
            '/diablo_system_status',
            10
        )

        self.required_nodes = [
            'diablo_ctrl_node',
            'diablo_motion_bridge_node',
            'camera_cmd_node',
            'tts_feedback_node',
            'voice_command_mapper_node',
            'voice_command_node',
        ]

        self.required_topics = [
            '/diablo/MotionCmd',
            '/diablo/sensor/Battery',
            '/diablo/sensor/Motors',
            '/diablo_motion_request',
            '/diablo_safe_cmd',
            '/diablo_feedback',
            '/voice_cmd_de',
            '/voice_text',
            '/camera/cmd',
        ]

        self.timer = self.create_timer(
            1.0,
            self.check_system
        )

        self.get_logger().info(
            'Diablo System State Node aktiv: /diablo_system_status'
        )

    def check_system(self):

        nodes = self.get_node_names()
        topics = [name for name, _types in self.get_topic_names_and_types()]

        node_ok = sum(
            1 for n in self.required_nodes
            if n in nodes
        )

        topic_ok = sum(
            1 for t in self.required_topics
            if t in topics
        )

        total = len(self.required_nodes) + len(self.required_topics)
        current = node_ok + topic_ok

        percent = int((current / total) * 100)

        if percent >= 95:
            state = 'READY'
        elif percent >= 60:
            state = 'STARTING'
        else:
            state = 'BOOTING'

        msg = String()

        msg.data = (
            f'{state} {percent}% | '
            f'NODES {node_ok}/{len(self.required_nodes)} | '
            f'TOPICS {topic_ok}/{len(self.required_topics)} | '
            f'MOTION LOCKED | CAM OFF | VOICE OFF | TRACK OFF | CHAT OFF'
        )

        self.pub.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = DiabloSystemStateNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
