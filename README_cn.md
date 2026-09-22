# hex_ros_demo_composite — 底盘与双臂全身阻抗组合启动包

**中文** | [English](README.md)

## 目录

- [项目概述](#项目概述)
- [快速使用](#快速使用)
- [安装](#安装)
- [启动内容](#启动内容)
- [话题接口](#话题接口)
- [启动参数](#启动参数)
- [项目结构](#项目结构)

## 项目概述

`hex_ros_demo_composite` 是 Maver X4 底盘与双机械臂的真机组合启动包。它将现有驱动、阻抗控制、手柄和键盘 launch 组织到统一命名空间中。

一次启动包含：

- Maver X4 底盘驱动与底盘阻抗控制；
- 左右 Archer Y6 / Firefly Y6 驱动与机械臂阻抗控制；
- 底盘手柄输入、共享键盘和可选 RViz。

本包支持 **ROS 2 Humble**，兼容 **ROS 1 Noetic**。

## 快速使用

> 请先完成[安装](#安装)，再选择以下启动入口。

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

## 安装

### 前置条件

- 已安装 **ROS 2 Humble**；使用 ROS 1 时安装 **ROS 1 Noetic**。
- 已安装 Python 3、`pip3`、Git，以及所选 ROS 版本的构建工具。
- 真机场景需确保设备网络可达，并准备好实际 IP、端口和设备型号。

### 1. 安装组合启动所需 Python 依赖

```shell
pip3 install \
    'hex-util-msg>=0.1.0' \
    'hex-util-ros>=0.1.0' \
    'hex-util-runtime>=0.1.0' \
    'hex-driver-robot>=0.1.0' \
    evdev
```

### 2. 创建并进入工作空间

```shell
mkdir -p <your_ws>/src
cd <your_ws>/src
```

### 3. 克隆组合启动所需 ROS 包

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

### 4. 编译包

**ROS 2：**

```shell
source /opt/ros/humble/setup.bash
cd <your_ws>
colcon build
source install/setup.bash
```

**ROS 1：**

```shell
source /opt/ros/noetic/setup.bash
cd <your_ws>
catkin_make
source devel/setup.bash
```

## 启动内容

完整 launch 会启动：

- Maver X4 底盘驱动、底盘阻抗控制节点和底盘手柄输入；
- `left` 与 `right` 命名空间下的机械臂驱动和阻抗控制节点；
- 一个共享键盘节点，发布 `/teleop_keyboard_state`；
- 可选的 RViz。左右机械臂可分别通过 `left_robot_type` 和 `right_robot_type` 选择 Archer Y6 或 Firefly Y6。

按一次 **`q`** 会同时触发底盘、左臂和右臂阻抗节点的退出与稳定流程；请保持整个运动区域畅通，直到三者完成。

底盘手柄映射：左摇杆纵轴控制前后（X），左摇杆横轴控制横移（Y），右摇杆横轴控制旋转（yaw）；`Y` / `X` 增大 / 减小线速度，`B` / `A` 增大 / 减小角速度。可用 `ros2 topic echo /chassis/cmd_vel`（ROS 1 使用 `rostopic echo /chassis/cmd_vel`）确认命令输出。

手柄的 `device_path` 由 `hex_ros_teleop_joystick` 管理。自动检测失败或存在多个输入设备时，请在 `<your_ws>/src/hex_ros_teleop_joystick/config/ros2/params.yaml` 或 `<your_ws>/src/hex_ros_teleop_joystick/config/ros1/params.yaml` 中设置，然后重新构建并 source 工作空间。

## 话题接口

下表汇总组合启动后的节点连接关系。

| 话题 | 发布者 | 订阅者 | 类型 | 说明 |
|------|--------|--------|------|------|
| `/chassis/cmd_vel` | 手柄节点 | 底盘阻抗节点 | `geometry_msgs/msg/Twist` | 底盘速度命令 |
| `/chassis/chs_ctrl` | 底盘阻抗节点 | 底盘驱动 | `hex_ros_msgs/msg/HexRosRoboChsCtrlStamped` | 底盘控制消息 |
| `/left/manip_ctrl` | 左臂阻抗节点 | 左臂驱动 | `hex_ros_msgs/msg/HexRosRoboManipCtrlStamped` | 左臂控制消息 |
| `/right/manip_ctrl` | 右臂阻抗节点 | 右臂驱动 | `hex_ros_msgs/msg/HexRosRoboManipCtrlStamped` | 右臂控制消息 |
| `/chassis/chs_state` | 底盘驱动 | 底盘阻抗节点 | `hex_ros_msgs/msg/HexRosRoboChsStateStamped` | 底盘状态消息 |
| `/left/manip_state` | 左臂驱动 | 左臂阻抗节点 | `hex_ros_msgs/msg/HexRosRoboManipStateStamped` | 左臂状态消息 |
| `/right/manip_state` | 右臂驱动 | 右臂阻抗节点 | `hex_ros_msgs/msg/HexRosRoboManipStateStamped` | 右臂状态消息 |
| `/teleop_keyboard_state` | 键盘节点 | 底盘与左右臂阻抗节点 | `hex_ros_msgs/msg/HexRosTeleopKeyboardStateStamped` | 键盘状态消息 |

各话题的实际相对名称由被引入的 driver 和 impedance launch 定义；上述路径是当前组合 launch 的命名空间结果。

## 启动参数

| 参数 | 说明 |
|------|------|
| `chassis_robot_host` | 底盘控制器 IP 地址 |
| `chassis_robot_port` | 底盘控制器端口 |
| `left_robot_type` | 左臂类型：`archer` 或 `firefly` |
| `left_robot_host` | 左臂控制器 IP 地址 |
| `left_robot_port` | 左臂控制器端口 |
| `left_robot_grip_type` | `gp100`、`gp80`、`gr100` 或 `empty` |
| `right_robot_type` | 右臂类型：`archer` 或 `firefly` |
| `right_robot_host` | 右臂控制器 IP 地址 |
| `right_robot_port` | 右臂控制器端口 |
| `right_robot_grip_type` | `gp100`、`gp80`、`gr100` 或 `empty` |
| `use_cmd` | 是否启用手柄命令输入；ROS 1 固定为 `true` |
| `rviz` | 是否启动 RViz；仅 ROS 2 顶层 launch 提供该参数 |

## 项目结构

```text
hex_ros_demo_composite/
├── config/
│   ├── ros1/
│   └── ros2/
├── hex_ros_demo_composite/
│   └── __init__.py                          # Python 包初始化文件
├── launch/
│   ├── ros1/
│   │   └── real_whole_body_impedance.launch # ROS 1 组合启动文件
│   └── ros2/
│       └── real_whole_body_impedance.launch.py # ROS 2 组合启动文件
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
