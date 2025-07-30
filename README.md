# TurtleBot3 Distance and Navigation Error Calculator

This ROS node calculates the total distance traveled by a TurtleBot3 robot and the navigation error after the robot completes its path. It subscribes to `/odom` for real-time odometry data, `/move_base_simple/goal` for target destination, and `/amcl_pose` for final pose estimation. The script logs the robot's path, total distance traveled, duration of navigation, average speed, and error between the target and final position.

## Features
- Calculates total traveled distance using odometry data.
- Records start and end position using AMCL.
- Captures target goal from RViz interaction.
- Calculates average speed and navigation error.
- Outputs summary logs for further analysis.

## Topics Subscribed
- `/odom` – for live odometry updates.
- `/move_base_simple/goal` – for setting navigation target.
- `/amcl_pose` – for final position after navigation completes.

## Requirements
- ROS Noetic (or compatible)
- Python 3
- Packages:
  - `rospy`
  - `geometry_msgs`
  - `nav_msgs`
  - `math`
  - `time`

## Usage
```bash
rosrun your_package_name distance_calculator.py
```
Make sure to make the script executable:
```bash
chmod +x distance_calculator.py
```

## Author
Rifky Andigta Al-Fathir.
