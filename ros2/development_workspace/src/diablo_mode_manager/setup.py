from setuptools import setup, find_packages

package_name = 'diablo_mode_manager'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='GVM',
    maintainer_email='opensource@invalid.example',
    description='Diablo central mode manager',
    license='MIT',
    entry_points={
        'console_scripts': [
            'mode_manager_node = diablo_mode_manager.mode_manager_node:main',
            'voice_runtime_manager_node = diablo_mode_manager.voice_runtime_manager_node:main',
        ],
    },
)
