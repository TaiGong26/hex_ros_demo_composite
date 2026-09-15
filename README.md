# hex_ros_demo_composite
[**中文**](README_cn.md) | **English**

## Table of Contents

- [1. About](#1-about)
- [2. Launch Contents](#2-launch-contents)
- [3. Topics](#3-topics)
- [4. Launch Arguments](#4-launch-arguments)
- [5. Dependencies](#5-dependencies)
- [6. Quick Start](#6-quick-start)

## 1. About

This package provides a whole-body impedance bringup that starts the Maver X4 chassis and impedance-controlled real arms on the left and right sides. It only composes existing driver, teleoperation, and impedance launches; it does not provide an independent control node.

The current real-robot composition provides:

- Maver X4 chassis;
- independently selectable Archer Y6 or Firefly Y6 left and right arms;
- one shared keyboard node;
- joystick input for chassis velocity commands.

## 2. Launch Contents

```text
hex_ros_demo_composite/
├── launch/
│   ├── ros1/real_whole_body_impedance.launch
│   └── ros2/real_whole_body_impedance.launch.py
├── config/                  # Reserved configuration directories; not read by the current composition
├── CMakeLists.txt
├── setup.py
└── package.xml
```

## 3. Topics

The main topics after startup are:

| Direction | Topic | Description |
|-----------|-------|-------------|
| Published | `/chassis/cmd_vel` | Chassis joystick velocity command |
| Published | `/chassis/chs_ctrl` | Chassis impedance control command |
| Published | `/left/manip_ctrl` | Left arm impedance control command |
| Published | `/right/manip_ctrl` | Right arm impedance control command |
| Subscribed | `/chassis/chs_state` | Chassis state |
| Subscribed | `/left/manip_state` | Left arm state |
| Subscribed | `/right/manip_state` | Right arm state |
| Subscribed | `/teleop_keyboard_state` | Shared keyboard state |

The exact relative names are defined by the included driver and impedance launches; the paths above are the results of the namespaces used by the current composition.

## 4. Launch Arguments

Chassis arguments:

| Argument | Description |
|----------|-------------|
| `chassis_robot_host` | Chassis controller IP address |
| `chassis_robot_port` | Chassis controller port |

Left arm arguments:

| Argument | Description |
|----------|-------------|
| `left_robot_type` | `archer` or `firefly` |
| `left_robot_host` | Left arm controller IP address |
| `left_robot_port` | Left arm controller port |
| `left_robot_grip_type` | `gp100`, `gp80`, `gr100`, or `empty` |

Right arm arguments:

| Argument | Description |
|----------|-------------|
| `right_robot_type` | `archer` or `firefly` |
| `right_robot_host` | Right arm controller IP address |
| `right_robot_port` | Right arm controller port |
| `right_robot_grip_type` | `gp100`, `gp80`, `gr100`, or `empty` |

Other arguments:

| Argument | Description |
|----------|-------------|
| `use_cmd` | Enable joystick command input |
| `rviz` | Start the RViz instance provided by the chassis launch |

## 5. Dependencies

### Python Packages

```shell
pip3 install 'hex-util-msg>=0.1.0'
pip3 install 'hex-util-ros>=0.1.0a4'
pip3 install 'hex-driver-robot>=0.1.0'
```

### ROS Packages

```shell
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

Dependency responsibilities:

- `hex_ros_demo_arm_impedance`: arm impedance nodes and parameters for the left and right arms;
- `hex_ros_demo_chassis_impedance`: Maver X4 chassis impedance node and parameters;
- `hex_ros_robot_arm`: Archer Y6 / Firefly Y6 arm drivers;
- `hex_ros_robot_chassis`: Maver X4 chassis driver;
- `hex_ros_teleop_joystick`: joystick input node;
- `hex_ros_teleop_keyboard`: shared keyboard input node;
- `hex_ros_urdf_archer_y6`: arm model resources;
- `hex_ros_urdf_maver_x4`: chassis model resources.

## 6. Quick Start

### ROS 1

Open the following file first:

```text
launch/ros1/real_whole_body_impedance.launch
```

Edit these arguments for the actual devices:

```xml
<arg name="chassis_robot_host" default="192.168.1.100"/>
<arg name="chassis_robot_port" default="8439"/>
<arg name="left_robot_type" default="archer"/>
<arg name="left_robot_host" default="192.168.1.100"/>
<arg name="left_robot_port" default="8439"/>
<arg name="left_robot_grip_type" default="empty"/>
<arg name="right_robot_type" default="archer"/>
<arg name="right_robot_host" default="192.168.1.100"/>
<arg name="right_robot_port" default="9439"/>
<arg name="right_robot_grip_type" default="empty"/>
```

Then build and launch:

```shell
source /opt/ros/noetic/setup.bash
cd <your_ws>
catkin_make
source devel/setup.bash
roslaunch hex_ros_demo_composite real_whole_body_impedance.launch
```

### ROS 2

Open the following file first:

```text
launch/ros2/real_whole_body_impedance.launch.py
```

Edit the `default_value` values in these `DeclareLaunchArgument` declarations:

```python
chassis_host_arg = DeclareLaunchArgument(
    name='chassis_robot_host', default_value='192.168.1.100')
chassis_port_arg = DeclareLaunchArgument(
    name='chassis_robot_port', default_value='8439')
left_robot_type_arg = DeclareLaunchArgument(
    name='left_robot_type', default_value='firefly')
left_host_arg = DeclareLaunchArgument(
    name='left_robot_host', default_value='192.168.1.100')
left_port_arg = DeclareLaunchArgument(
    name='left_robot_port', default_value='8439')
left_grip_arg = DeclareLaunchArgument(
    name='left_robot_grip_type', default_value='empty')
right_robot_type_arg = DeclareLaunchArgument(
    name='right_robot_type', default_value='firefly')
right_host_arg = DeclareLaunchArgument(
    name='right_robot_host', default_value='192.168.1.100')
right_port_arg = DeclareLaunchArgument(
    name='right_robot_port', default_value='9439')
right_grip_arg = DeclareLaunchArgument(
    name='right_robot_grip_type', default_value='empty')
```

After editing, build and launch:

```shell
source /opt/ros/humble/setup.bash
cd <your_ws>
colcon build
source install/setup.bash
ros2 launch hex_ros_demo_composite real_whole_body_impedance.launch.py
```

Only one keyboard node is started, using the shared `/teleop_keyboard_state` topic. Press **`q`** to run the impedance exit and settling sequence. Verify emergency-stop operation and validate parameters and gains in a safe area before use.
