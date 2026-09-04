from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


def generate_launch_description():
    return LaunchDescription([

        # Argus Reset (wichtig)
        ExecuteProcess(
            cmd=['sudo', 'systemctl', 'restart', 'nvargus-daemon'],
            shell=True
        ),

        # Camera Node
        Node(
            package='diablo_camera',
            executable='camera_node',
            name='camera_node',
            output='screen'
        ),

        # Command Node
        Node(
            package='diablo_camera',
            executable='camera_cmd_node',
            name='camera_cmd_node',
            output='screen'
        ),
    ])
