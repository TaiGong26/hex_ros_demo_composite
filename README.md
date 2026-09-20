# hex_ros_demo_composite — Chassis and Dual-Arm Whole-Body Impedance Launcher

[中文](README_cn.md) | **English**

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Launch Contents](#launch-contents)
- [Topics](#topics)
- [Launch Arguments](#launch-arguments)
- [Project Structure](#project-structure)

## Overview

`hex_ros_demo_composite` is a real-robot bringup package for a Maver X4 chassis with two arms. It organizes existing driver, impedance-control, joystick, and keyboard launches under consistent namespaces.

A single launch starts:

- the Maver X4 driver and chassis impedance control;
- left and right Archer Y6 or Firefly Y6 drivers and arm impedance control;
- chassis joystick input, one shared keyboard, and optional RViz.

This package supports **ROS 2 Humble** and is compatible with **ROS 1 Noetic**.

## Quick Start

> Complete [Installation](#installation) before launching.

> All `192.168.1.x` addresses in this document are examples; replace them with actual device addresses. This launch moves the chassis and arms. Clear the operating area, verify the emergency stop, and validate with low-risk settings first.

### ROS 2

```shell
ros2 launch hex_ros_demo_composite real_whole_body_impedance.launch.py \
    chassis_robot_host:=192.168.1.100 chassis_robot_port:=8439 \
    left_robot_host:=192.168.1.100 left_robot_port:=8439 left_robot_type:=firefly left_robot_grip_type:=empty \
    right_robot_host:=192.168.1.100 right_robot_port:=9439 right_robot_type:=firefly right_robot_grip_type:=empty \
    use_cmd:=true rviz:=true
```

### ROS 1

```shell
roslaunch hex_ros_demo_composite real_whole_body_impedance.launch \
    chassis_robot_host:=192.168.1.100 chassis_robot_port:=8439 \
    left_robot_host:=192.168.1.100 left_robot_port:=8439 left_robot_type:=firefly left_robot_grip_type:=empty \
    right_robot_host:=192.168.1.100 right_robot_port:=9439 right_robot_type:=firefly right_robot_grip_type:=empty
```

## Installation

### Prerequisites

- **ROS 2 Humble** is installed; use **ROS 1 Noetic** for ROS 1 compatibility.
- Python 3, `pip3`, Git, and the build tools for the selected ROS version are installed.
- For real-hardware scenarios, devices are reachable and the actual IP addresses, ports, and device models are known.

### 1. Install Python Dependencies for the Launch Stack

```shell
pip3 install \
    'hex-util-msg>=0.1.0' \
    'hex-util-ros>=0.1.0' \
    'hex-util-runtime>=0.1.0' \
    'hex-driver-robot>=0.1.0' \
    evdev
```

### 2. Create and Enter the Workspace

```shell
mkdir -p <your_ws>/src
cd <your_ws>/src
```

### 3. Clone ROS Packages for the Launch Stack

```shell
git clone https://github.com/hexfellow/hex_ros_msgs.git
git clone https://github.com/hexfellow/hex_ros_demo_composite.git
git clone https://github.com/hexfellow/hex_ros_demo_arm_impedance.git
git clone https://github.com/hexfellow/hex_ros_demo_chassis_impedance.git
git clone https://github.com/hexfellow/hex_ros_robot_arm.git
git clone https://github.com/hexfellow/hex_ros_robot_chassis.git
git clone https://github.com/hexfellow/hex_ros_teleop_joystick.git
git clone https://github.com/hexfellow/hex_ros_teleop_keyboard.git
git clone https://github.com/hexfellow/hex_ros_urdf_archer_y6.git
git clone https://github.com/hexfellow/hex_ros_urdf_maver_x4.git
```

### 4. Build

**ROS 2:**

```shell
source /opt/ros/humble/setup.bash
cd <your_ws>
colcon build
source install/setup.bash
```

**ROS 1:**

```shell
source /opt/ros/noetic/setup.bash
cd <your_ws>
catkin_make
source devel/setup.bash
```

## Launch Contents

The complete launch starts:

- the Maver X4 chassis driver, chassis impedance node, and chassis joystick input;
- arm drivers and impedance nodes in the `left` and `right` namespaces;
- one shared keyboard node publishing `/teleop_keyboard_state`;
- optional RViz. Select Archer Y6 or Firefly Y6 independently with `left_robot_type` and `right_robot_type`.

Press **`q`** once to trigger the chassis and both arm impedance nodes to exit and settle together. Keep the entire operating area clear until all three have finished.

Chassis joystick mapping: the left-stick vertical axis commands forward/backward X motion, the left-stick horizontal axis commands lateral Y motion, and the right-stick horizontal axis commands yaw. `Y` / `X` increase / decrease linear speed; `B` / `A` increase / decrease angular speed. Verify output with `ros2 topic echo /chassis/cmd_vel` (ROS 1: `rostopic echo /chassis/cmd_vel`).

`hex_ros_teleop_joystick` manages the joystick `device_path`. If auto-detection fails or multiple input devices are present, set it in `<your_ws>/src/hex_ros_teleop_joystick/config/ros2/params.yaml` or `<your_ws>/src/hex_ros_teleop_joystick/config/ros1/params.yaml`, then rebuild and source the workspace.

## Topics

The table below summarizes node connections created by the composition.

| Topic | Publisher | Subscriber | Type | Description |
|-------|-----------|------------|------|-------------|
| `/chassis/cmd_vel` | Joystick node | Chassis impedance node | `geometry_msgs/msg/Twist` | Chassis velocity command |
| `/chassis/chs_ctrl` | Chassis impedance node | Chassis driver | `hex_ros_msgs/msg/HexRosRoboChsCtrlStamped` | Chassis control message |
| `/left/manip_ctrl` | Left arm impedance node | Left arm driver | `hex_ros_msgs/msg/HexRosRoboManipCtrlStamped` | Left arm control message |
| `/right/manip_ctrl` | Right arm impedance node | Right arm driver | `hex_ros_msgs/msg/HexRosRoboManipCtrlStamped` | Right arm control message |
| `/chassis/chs_state` | Chassis driver | Chassis impedance node | `hex_ros_msgs/msg/HexRosRoboChsStateStamped` | Chassis state message |
| `/left/manip_state` | Left arm driver | Left arm impedance node | `hex_ros_msgs/msg/HexRosRoboManipStateStamped` | Left arm state message |
| `/right/manip_state` | Right arm driver | Right arm impedance node | `hex_ros_msgs/msg/HexRosRoboManipStateStamped` | Right arm state message |
| `/teleop_keyboard_state` | Keyboard node | Chassis and both arm impedance nodes | `hex_ros_msgs/msg/HexRosTeleopKeyboardStateStamped` | Keyboard state message |

The exact relative names are defined by the included driver and impedance launches; the paths above are the results of the namespaces used by the current composition.

## Launch Arguments

| Argument | Description |
|----------|-------------|
| `chassis_robot_host` | Chassis controller IP address |
| `chassis_robot_port` | Chassis controller port |
| `left_robot_type` | Left arm type: `archer` or `firefly` |
| `left_robot_host` | Left arm controller IP address |
| `left_robot_port` | Left arm controller port |
| `left_robot_grip_type` | `gp100`, `gp80`, `gr100`, or `empty` |
| `right_robot_type` | Right arm type: `archer` or `firefly` |
| `right_robot_host` | Right arm controller IP address |
| `right_robot_port` | Right arm controller port |
| `right_robot_grip_type` | `gp100`, `gp80`, `gr100`, or `empty` |
| `use_cmd` | Enable joystick command input; fixed to `true` in ROS 1 |
| `rviz` | Start RViz; exposed only by the top-level ROS 2 launch |

## Project Structure

```text
hex_ros_demo_composite/
├── config/
│   ├── ros1/
│   └── ros2/
├── hex_ros_demo_composite/
│   └── __init__.py                          # Python package initializer
├── launch/
│   ├── ros1/
│   │   └── real_whole_body_impedance.launch # ROS 1 composition launch file
│   └── ros2/
│       └── real_whole_body_impedance.launch.py # ROS 2 composition launch file
├── resource/
│   └── hex_ros_demo_composite               
├── .gitignore
├── CMakeLists.txt
├── LICENSE
├── package.xml
├── README_cn.md
├── README.md
├── setup.cfg
└── setup.py
```
