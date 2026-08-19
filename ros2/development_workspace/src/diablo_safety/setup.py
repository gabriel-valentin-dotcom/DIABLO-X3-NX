from setuptools import setup

package_name = 'diablo_safety'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='GVM',
    maintainer_email='gvm@diablo-x3-nx.invalid',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'realsense_safety_node = diablo_safety.realsense_safety_node:main',
            'diablo_system_state_node = diablo_safety.diablo_system_state_node:main',
        ],
    },
)
