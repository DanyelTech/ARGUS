import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    package_path = get_package_share_directory('argus_description')

    xacro_file = os.path.join(
        package_path,
        'urdf',
        'argus_arm.urdf.xacro'
    )

    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            xacro_file
        ]),
        value_type=str
    )

    return LaunchDescription([

        # Publish the robot's transformations
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description
            }]
        ),

        # Joint control sliders
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),

        # 3D visualization
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=[
                '-d',
                os.path.join(package_path, 'rviz', 'argus.rviz')
            ],
            output='screen'
        )

    ])
