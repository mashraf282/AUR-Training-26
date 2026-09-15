import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Find the path to the installed YAML file
    pkg_share = get_package_share_directory('ROS2 Task')
    param_file = os.path.join(pkg_share, 'config', 'params.yaml')

    control_node = Node(
        package='ROS2 Task',
        executable='go_to_goal',
        name='go_to_goal',
        output='screen',
        parameters=[param_file]
    )

    client_node = Node(
        package='ROS2 Task',
        executable='turtle_toggle_client',
        name='turtle_toggle_client',
        output='screen'
    )

    turtle_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim_node',
        output='screen'
    )

    return LaunchDescription([
        control_node,
        client_node,
        turtle_node
    ])