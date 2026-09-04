from setuptools import setup

package_name = 'diablo_voice_command'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],

    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],

    install_requires=['setuptools'],
    zip_safe=True,

    maintainer='diablo',
    maintainer_email='diablo@example.com',

    description='DIABLO voice command and feedback nodes',

    license='MIT',

    entry_points={
        'console_scripts': [

            'voice_command_node = diablo_voice_command.voice_command_node:main',

            'beep_feedback_node = diablo_voice_command.beep_feedback_node:main',

            'voice_confirm_node = diablo_voice_command.voice_confirm_node:main',

            'tts_feedback_node = diablo_voice_command.tts_feedback_node:main',

            'voice_command_mapper_node = diablo_voice_command.voice_command_mapper_node:main',

            'diablo_action_node = diablo_voice_command.diablo_action_node:main',

            'safe_voice_pose_node = diablo_voice_command.safe_voice_pose_node:main',

        ],
    },
)
