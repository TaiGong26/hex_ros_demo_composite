#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################
# Copyright 2026 taigong26. All rights reserved.
# Author: taigong26 thetaigon@qq.com
# Date  : 2026-09-11
################################################################

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import PythonExpression
from launch_ros.actions import PushRosNamespace
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    arm_pkg_path = FindPackageShare('hex_ros_robot_arm')
    arm_impedance_pkg_path = FindPackageShare('hex_ros_demo_arm_impedance')
    chassis_pkg_path = FindPackageShare('hex_ros_robot_chassis')
    chassis_impedance_pkg_path = FindPackageShare(
        'hex_ros_demo_chassis_impedance')
    joystick_pkg_path = FindPackageShare('hex_ros_teleop_joystick')
    keyboard_pkg_path = FindPackageShare('hex_ros_teleop_keyboard')

    chassis_host_arg = DeclareLaunchArgument(
        name='chassis_robot_host',
        default_value='192.168.1.100',
        description='Chassis controller IP address')
    chassis_port_arg = DeclareLaunchArgument(
        name='chassis_robot_port',
        default_value='8439',
        description='Chassis controller WebSocket port')

    left_type_arg = DeclareLaunchArgument(
        name='left_robot_type',
        default_value='firefly',
        choices=['archer', 'firefly'],
        description='Left robot arm type')
    left_host_arg = DeclareLaunchArgument(
        name='left_robot_host',
        default_value='172.18.20.80',
        description='Left robot controller IP address')
    left_port_arg = DeclareLaunchArgument(
        name='left_robot_port',
        default_value='8439',
        description='Left robot controller WebSocket port')
    left_grip_arg = DeclareLaunchArgument(
        name='left_robot_grip_type',
        default_value='empty',
        choices=['gp100', 'gp80', 'gr100', 'empty'],
        description='Left robot grip type')

    right_type_arg = DeclareLaunchArgument(
        name='right_robot_type',
        default_value='firefly',
        choices=['archer', 'firefly'],
        description='Right robot arm type')
    right_host_arg = DeclareLaunchArgument(
        name='right_robot_host',
        default_value='172.18.20.80',
        description='Right robot controller IP address')
    right_port_arg = DeclareLaunchArgument(
        name='right_robot_port',
        default_value='9439',
        description='Right robot controller WebSocket port')
    right_grip_arg = DeclareLaunchArgument(
        name='right_robot_grip_type',
        default_value='empty',
        choices=['gp100', 'gp80', 'gr100', 'empty'],
        description='Right robot grip type')

    chassis_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([chassis_pkg_path, 'maver.launch.py'])),
        launch_arguments={
            'robot_host': LaunchConfiguration('chassis_robot_host'),
            'robot_port': LaunchConfiguration('chassis_robot_port'),
        }.items(),
    )
    chassis_impedance_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                chassis_impedance_pkg_path,
                'chassis_impedance_maver_x4.launch.py',
            ])),
        launch_arguments={'use_sim_time': 'false'}.items(),
    )
    joystick_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [joystick_pkg_path, 'teleop_joystick.launch.py'])),
        launch_arguments={
            'use_cmd': 'true',
            'cmd_topic': '/chassis/cmd_vel',
        }.items(),
    )
    keyboard_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [keyboard_pkg_path, 'teleop_keyboard.launch.py'])))

    left_robot_file = PythonExpression(
        ['"', LaunchConfiguration('left_robot_type'), '.launch.py"'])
    right_robot_file = PythonExpression(
        ['"', LaunchConfiguration('right_robot_type'), '.launch.py"'])
    left_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([arm_pkg_path, left_robot_file])),
        launch_arguments={
            'robot_host': LaunchConfiguration('left_robot_host'),
            'robot_port': LaunchConfiguration('left_robot_port'),
            'robot_grip_type': LaunchConfiguration('left_robot_grip_type'),
            'test': 'false',
        }.items(),
    )
    right_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([arm_pkg_path, right_robot_file])),
        launch_arguments={
            'robot_host': LaunchConfiguration('right_robot_host'),
            'robot_port': LaunchConfiguration('right_robot_port'),
            'robot_grip_type': LaunchConfiguration('right_robot_grip_type'),
            'test': 'false',
        }.items(),
    )
    left_impedance_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                arm_impedance_pkg_path,
                'arm_impedance.launch.py',
            ])),
        launch_arguments={'use_sim_time': 'false'}.items(),
    )
    right_impedance_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                arm_impedance_pkg_path,
                'arm_impedance.launch.py',
            ])),
        launch_arguments={'use_sim_time': 'false'}.items(),
    )

    chassis_group = GroupAction([
        PushRosNamespace('chassis'),
        chassis_driver_launch,
        chassis_impedance_launch,
    ])
    left_group = GroupAction([
        PushRosNamespace('left'),
        left_driver_launch,
        left_impedance_launch,
    ])
    right_group = GroupAction([
        PushRosNamespace('right'),
        right_driver_launch,
        right_impedance_launch,
    ])

    return LaunchDescription([
        chassis_host_arg,
        chassis_port_arg,
        left_type_arg,
        left_host_arg,
        left_port_arg,
        left_grip_arg,
        right_type_arg,
        right_host_arg,
        right_port_arg,
        right_grip_arg,
        keyboard_launch,
        joystick_launch,
        chassis_group,
        left_group,
        right_group,
    ])
