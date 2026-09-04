from setuptools import setup

package_name = 'diablo_camera'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/camera_system.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='GVM',
    maintainer_email='opensource@invalid.example',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'follow_action_node = diablo_camera.follow_action_node:main',
            'follow_manager_node = diablo_camera.follow_manager_node:main',
            'gesture_ros_node = diablo_camera.gesture_ros_node:main',
            'auto_supervisor_node = diablo_camera.auto_supervisor_node:main',
            'auto_manager_node = diablo_camera.auto_manager_node:main',
            'realsense_preview_node = diablo_camera.realsense_preview_node:main',
            'vision_track_node = diablo_camera.vision_track_node:main',
            'camera_node = diablo_camera.camera_node:main',
            'camera_preview_node = diablo_camera.camera_preview_node:main',
            'camera_cmd_node = diablo_camera.camera_cmd_node:main',
            'camera_manager_node = diablo_camera.camera_manager_node:main',
            'tracker_node = diablo_camera.tracker_node:main',
            'tracker_preview_node = diablo_camera.tracker_preview_node:main',
            'hand_gesture_preview_node = diablo_camera.hand_gesture_preview_node:main',
            'gesture_command_node = diablo_camera.gesture_command_node:main',
            'motor_stall_protect_node = diablo_camera.motor_stall_protect_node:main',
            'lidar_safety_node = diablo_camera.lidar_safety_node:main',
            'safety_bubble_node = diablo_camera.safety_bubble_node:main',
            'uwb_range_node = diablo_camera.uwb_range_node:main',
        ],
    },
)
