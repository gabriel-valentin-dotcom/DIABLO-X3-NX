from setuptools import setup

package_name = 'diablo_tracker'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='GVM',
    maintainer_email='gvm@diablo-x3-nx.invalid',
    description='DIABLO X3 UWB tracker node',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tracker_node = diablo_tracker.tracker_node:main',
        ],
    },
)
