# hex_ros_demo_composite
**中文** | [English](README.md)

## 目录

- [1. 包简介](#1-包简介)
- [2. 启动内容](#2-启动内容)
- [3. 话题接口](#3-话题接口)
- [4. 启动参数](#4-启动参数)
- [5. 依赖关系](#5-依赖关系)
- [6. 快速使用](#6-快速使用)

## 1. 包简介

这是 whole-body impedance 组合启动包，用于同时启动 Maver X4 底盘和左右两侧真实机械臂的阻抗控制。该包只负责组合已有 driver、teleop 和 impedance launch，不包含独立控制节点。

当前提供一个 ROS 1/ROS 2 对应的真机组合入口：

- 底盘：Maver X4；
- 左臂和右臂：可分别选择 Archer Y6 或 Firefly Y6；
- 键盘：只启动一个共享键盘节点；
- 手柄：用于底盘速度命令。

## 2. 启动内容

```text
hex_ros_demo_composite/
├── launch/
│   ├── ros1/real_whole_body_impedance.launch
│   └── ros2/real_whole_body_impedance.launch.py
├── config/                  # 预留配置目录，当前组合 launch 不读取自定义 YAML
├── CMakeLists.txt
├── setup.py
└── package.xml
```

## 3. 话题接口

启动后的主要话题如下：

| 方向 | 话题 | 说明 |
|------|------|------|
| 发布 | `/chassis/cmd_vel` | 底盘手柄速度命令 |
| 发布 | `/chassis/chs_ctrl` | 底盘阻抗控制命令 |
| 发布 | `/left/manip_ctrl` | 左臂阻抗控制命令 |
| 发布 | `/right/manip_ctrl` | 右臂阻抗控制命令 |
| 订阅 | `/chassis/chs_state` | 底盘状态 |
| 订阅 | `/left/manip_state` | 左臂状态 |
| 订阅 | `/right/manip_state` | 右臂状态 |
| 订阅 | `/teleop_keyboard_state` | 共享键盘状态 |

各话题的实际相对名称由被引入的 driver 和 impedance launch 定义；上述路径是当前组合 launch 的命名空间结果。

## 4. 启动参数

底盘参数：

| 参数 | 说明 |
|------|------|
| `chassis_robot_host` | 底盘控制器 IP 地址 |
| `chassis_robot_port` | 底盘控制器端口 |

左臂参数：

| 参数 | 说明 |
|------|------|
| `left_robot_type` | `archer` 或 `firefly` |
| `left_robot_host` | 左臂控制器 IP 地址 |
| `left_robot_port` | 左臂控制器端口 |
| `left_robot_grip_type` | `gp100`、`gp80`、`gr100` 或 `empty` |

右臂参数：

| 参数 | 说明 |
|------|------|
| `right_robot_type` | `archer` 或 `firefly` |
| `right_robot_host` | 右臂控制器 IP 地址 |
| `right_robot_port` | 右臂控制器端口 |
| `right_robot_grip_type` | `gp100`、`gp80`、`gr100` 或 `empty` |

其他参数：

| 参数 | 说明 |
|------|------|
| `use_cmd` | 是否启用手柄命令输入 |
| `rviz` | 是否启动底盘 launch 提供的 RViz |

## 5. 依赖关系

### Python 包

```shell
pip3 install 'hex-util-msg>=0.1.0'
pip3 install 'hex-util-ros>=0.1.0a4'
pip3 install 'hex-driver-robot>=0.1.0'
```

### ROS 包

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

依赖职责：

- `hex_ros_demo_arm_impedance`：左右机械臂阻抗控制节点和参数；
- `hex_ros_demo_chassis_impedance`：Maver X4 底盘阻抗控制节点和参数；
- `hex_ros_robot_arm`：Archer Y6 / Firefly Y6 机械臂 driver；
- `hex_ros_robot_chassis`：Maver X4 底盘 driver；
- `hex_ros_teleop_joystick`：手柄输入节点；
- `hex_ros_teleop_keyboard`：公共键盘输入节点；
- `hex_ros_urdf_archer_y6`：机械臂模型资源；
- `hex_ros_urdf_maver_x4`：底盘模型资源。

## 6. 快速使用

### ROS 1

先打开以下文件：

```text
launch/ros1/real_whole_body_impedance.launch
```

根据实际设备修改这些参数：

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

然后构建并启动：

```shell
source /opt/ros/noetic/setup.bash
cd <your_ws>
catkin_make
source devel/setup.bash
roslaunch hex_ros_demo_composite real_whole_body_impedance.launch
```

### ROS 2

先打开以下文件：

```text
launch/ros2/real_whole_body_impedance.launch.py
```

修改这些 `DeclareLaunchArgument` 中的 `default_value`：

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

修改完成后再构建并启动：

```shell
source /opt/ros/humble/setup.bash
cd <your_ws>
colcon build
source install/setup.bash
ros2 launch hex_ros_demo_composite real_whole_body_impedance.launch.py
```

键盘节点只启动一次，公共话题为 `/teleop_keyboard_state`。阻抗节点按 **`q`** 执行退出和归位流程。使用前请确认急停有效，并在安全区域验证参数和增益。
