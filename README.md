# ROS2 Obstacle Avoidance System

A ROS2 obstacle-avoidance demo built with Python and three communicating nodes: a distance sensor publisher, a motion controller, and a real-time monitor.

## Overview

The system demonstrates a simple reactive obstacle-avoidance architecture using ROS2 topics.

The current `sensor_node.py` generates simulated front-distance values for testing. These values are published to `/front_distance`, where the controller decides whether the robot should move forward or turn.

The motion command is published to `/cmd_vel`, and a monitoring node observes both topics to report the current robot state.

## Architecture

```text
sensor_node.py
     |
     |  /front_distance  (std_msgs/Float32)
     v
controller_node.py
     |
     |  /cmd_vel  (geometry_msgs/Twist)
     v
 Robot / Motion Layer

monitor_node.py
     ^
     |---- /front_distance
     |
     |---- /cmd_vel
```

## Nodes

### 1. Sensor Node

File: `sensor_node.py`

- Publishes front-distance values to `/front_distance`
- Uses `std_msgs/Float32`
- Publishes every 0.5 seconds
- Currently generates simulated values between 0.1 m and 2.0 m for testing

### 2. Controller Node

File: `controller_node.py`

- Subscribes to `/front_distance`
- Publishes velocity commands to `/cmd_vel`
- Uses `geometry_msgs/Twist`
- Uses a safe-distance threshold of `0.5 m`

Control logic:

```text
Distance > 0.5 m
    -> Move forward
    -> linear.x = 0.3
    -> angular.z = 0.0

Distance <= 0.5 m
    -> Turn to avoid obstacle
    -> linear.x = 0.0
    -> angular.z = 0.6
```

### 3. Monitor Node

File: `monitor_node.py`

The monitor subscribes to:

- `/front_distance`
- `/cmd_vel`

It reports the current distance and classifies the motion state as:

- `MOVING FORWARD`
- `TURNING`
- `STOPPED`

## ROS2 Topics

| Topic | Message Type | Purpose |
|---|---|---|
| `/front_distance` | `std_msgs/Float32` | Front obstacle distance |
| `/cmd_vel` | `geometry_msgs/Twist` | Linear and angular velocity commands |

## Technologies

- ROS2 (Humble)
- Python
- rclpy
- Publisher / Subscriber Architecture
- `std_msgs`
- `geometry_msgs`
- Reactive Robot Control

## Running the Demo

Source ROS2 in each terminal, then run the three nodes — one per terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run robot_three_nodes sensor_node
```

```bash
ros2 run robot_three_nodes controller_node
```

```bash
ros2 run robot_three_nodes monitor_node
```

## Example Behavior

When the simulated distance is greater than `0.5 m`, the controller publishes a forward velocity command.

When an obstacle is within `0.5 m`, the controller stops forward motion and publishes an angular velocity command to turn away from the obstacle.

```
[sensor_node]:     Front distance: 0.43 m
[controller_node]: Distance: 0.15 m -> TURNING (OBSTACLE AHEAD)
[monitor_node]:    [MONITOR] Distance: 0.34 m | State: TURNING
```

## Extending the Project

The simulated sensor publisher can be replaced with a real ultrasonic, LiDAR, or other distance-sensor interface while keeping the same `/front_distance` topic and controller architecture. Other possible extensions include multiple sensor directions (left/right), PID-based turning instead of a fixed angular velocity, and a Gazebo simulation to visualize the robot's motion.

## Author

**Mohammad Ahmad Elayyan**

- Email: [mohamadelayyan84@gmail.com](mailto:mohamadelayyan84@gmail.com)
- LinkedIn: https://www.linkedin.com/in/mohammadelayyan1
- GitHub: [MohammadElayyan117](https://github.com/MohammadElayyan117)
