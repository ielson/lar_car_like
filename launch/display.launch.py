from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    xacro_file = PathJoinSubstitution([
        FindPackageShare('lar_car_like2'),
        'urdf',
        'carlike.urdf.xacro'
    ])

    rviz_config_file = PathJoinSubstitution([
        FindPackageShare('lar_car_like2'),
        'rviz',
        'robot.rviz'
        ])

    # create slides to change the robots joints
    joint_state_publisher_node = Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        )

    # reads the urdf and publishes the robot frames
    robot_state_publisher_node = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro ', xacro_file])
            }]
        )

    rviz_node = Node(
            package='rviz2',
            executable='rviz2', 
            arguments=['-d', rviz_config_file],
        )

    nodes = [
            joint_state_publisher_node,
            robot_state_publisher_node,
            rviz_node
            ]

    return LaunchDescription(nodes)
