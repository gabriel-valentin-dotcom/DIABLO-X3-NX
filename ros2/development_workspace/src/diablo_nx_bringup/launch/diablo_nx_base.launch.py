from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='diablo_camera', executable='camera_cmd_node', name='camera_cmd_node', output='screen'),
        Node(package='diablo_voice_command', executable='command_router_node', name='command_router_node', output='screen'),
        Node(package='diablo_voice_command', executable='safety_gate_node', name='safety_gate_node', output='screen'),
        Node(package='diablo_voice_command', executable='beep_feedback_node', name='beep_feedback_node', output='screen'),
    ])
