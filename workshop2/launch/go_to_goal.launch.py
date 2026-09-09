import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Find the path to the installed YAML file
    pkg_share = get_package_share_directory('workshop2')
    param_file = os.path.join(pkg_share, 'config', 'params.yaml')

    # Define the node execution
    demo_node = Node(
        package='workshop2',
        executable='go_to_goal',
        name='go_to_goal',
        output='screen',
        parameters=[param_file]
    )

    return LaunchDescription([
        demo_node
    ])