import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'ROS2 Task'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bread',
    maintainer_email='adhamgaweesh@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'turtle_controller = ROS2 Task.turtle_controller:main',
            'go_to_goal = ROS2 Task.go_to_goal:main',
            'turtle_toggle_client = ROS2 Task.turtle_toggle_client:main',
        ],
    },
)
