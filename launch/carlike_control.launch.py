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

    controllers_file = PathJoinSubstitution([
        FindPackageShare('lar_car_like2'),
        'config',
        'controllers.yaml'
        ])

    robot_description = {
        'robot_description': Command(['xacro ', xacro_file])
    }

    # controllers
    steering_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'steering_position_controller',
            '--controller-manager',
            '/controller_manager',
        ],
    )

    wheel_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'wheel_velocity_controller',
            '--controller-manager',
            '/controller_manager',
        ],
    )

    joint_state_broadcaster_spawner = Node(
    package="controller_manager",
    executable="spawner",
    arguments=[
        "joint_state_broadcaster",
        "--controller-manager",
        "/controller_manager",
    ],
    )

    robot_controller_node = Node(
            package='controller_manager',
            executable='ros2_control_node', 
            output="both",
            parameters=[robot_description, controllers_file]
        )

    # reads the urdf and publishes the robot frames
    robot_state_publisher_node = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description]
        )

    rviz_node = Node(
            package='rviz2',
            executable='rviz2', 
            arguments=['-d', rviz_config_file],
        )

    nodes = [
            robot_controller_node,
            robot_state_publisher_node,
            rviz_node, 
            steering_controller_spawner,
            wheel_controller_spawner,
            joint_state_broadcaster_spawner
            ]

    return LaunchDescription(nodes)
