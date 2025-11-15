# Nav2_diffdrive_robot

This project demonstrates implementation of a differential drive robot simulation using Nav2 and rviz2.

# System Requirements

Ubuntu: 22.04 LTS
ROS 2: Jazzy Jalisco
Gazebo: Harmonic

Usage Prerequisites

Install required ROS 2 packages:
```
 sudo apt install ros-jazzy-robot-state-publisher \
                 ros-jazzy-joint-state-publisher \
                 ros-jazzy-xacro \
                 ros-jazzy-teleop-twist-keyboard \
                 ros-jazzy-ros-gz-sim \
                 ros-jazzy-ros-gz-bridge \
                 ros-jazzy-sensor-msgs \
                 ros-jazzy-rviz2
```
Installation & Setup

Create Workspace and Clone Repository

        mkdir -p my_ws/src && cd my_ws/src
        git clone https://github.com/sivapriya083/Autonomous_navigation.git 

Build the workspace
```
   cd .. colcon build
```
Source the Workspace
```
   source install/setup.bash
```

# Terminal 1 :- Launch Robot in Gazebo
```
    ros2 launch tortoisebot_gazebo custom_world.launch.py
```

# Terminal 2 :- launch rviz2
```rviz2 ```

#  Terminal 3: 
     ```ros2 run teleop_twist_keyboard teleop_twist_keyboard```

     
#  Terminal 4: 
     ```ros2 launch slam_toolbox online_async_launch.py   slam_params_file:=/home/sivapriya-arz-i012/task6/tortoisebot_ws/src/tortoisebot_localization/config/mapper_params_online_async.yaml   use_sim_time:=true```

     
#  Terminal 5: 
    ```ros2 run twist_mux twist_mux   --ros-args   --params-file /home/sivapriya-arz-i012/task6/tortoisebot_ws/src/tortoisebot_localization/config/twist_mux.yaml   -r cmd_vel_out:=diff_cont/cmd_vel_unstamped```
    
#  Terminal 6: 
    ``ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true```



# special mention : Twist_mux

twist_mux is a ROS package that combines multiple geometry_msgs::Twist (velocity) commands into a single output topic, allowing for prioritized control of a robot from different sources like a joystick, keyboard, or autonomous navigation system. It works by selecting the highest priority command that is not locked or timed out, which enables features like an emergency stop taking precedence over a joystick, and autonomous navigation resuming when the manual control is released.


reference :- Articulated Robotics





















 
