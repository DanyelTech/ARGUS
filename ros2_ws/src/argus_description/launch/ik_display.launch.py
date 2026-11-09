
"""Launch the ARGUS IK node, robot-state publisher, and RViz."""
from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription

from launch_ros.actions import Node

import xacro


def generate_launch_description():
    """Create the ARGUS IK visualization launch description."""
    description_dir = Path(
        get_package_share_directory('argus_description')
    )

    urdf_path = (
        description_dir / 'urdf' / 'argus_arm.urdf.xacro'
    )

    rviz_config = (
        description_dir / 'rviz' / 'argus.rviz'
    )

    robot_description = xacro.process_file(
        str(urdf_path)
    ).toxml()

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description}
        ],
        output='screen',
    )

    ik_node = Node(
        package='argus_bringup',
        executable='ik_node',
        name='ik_node',
        remappings=[
            ('/argus/joint_commands', '/joint_states')
        ],
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', str(rviz_config)],
        output='screen',
    )

    return LaunchDescription([
        robot_state_publisher,
        ik_node,
        rviz,
    ])
