# ROS-Blender-Addon
Add-on to use Blender for visualization with ROS (Robot Operating System).


## Install instructions
- Download [ROS_addon.zip](https://github.com/ahmad-aljabali/ROS-Blender-Addon/raw/master/ROS_addon.zip) to install it from blender->Edit->Preferences->Add-ons->Install.
- Install Python dependencies
```Shell
sudo apt install python3-rospy python3-opencv
```

## Screenshots of UI
![Screenshot](https://github.com/ahmad-aljabali/ROS-Blender-Addon/blob/master/ROS_addon%20screenshot.png)


## Features
- Control and Publish objects Location using [geometry_msgs/Point](https://docs.ros.org/api/geometry_msgs/html/msg/Point.html)

- Control and Publish objects Rotation using [geometry_msgs/Quaternion](https://docs.ros.org/api/geometry_msgs/html/msg/Quaternion.html)

- Control and Publish objects Location & Rotation using [geometry_msgs/Pose](https://docs.ros.org/api/geometry_msgs/html/msg/Pose.html)

- Publish Rendered Image Stream using [sensor_msgs/Image](https://docs.ros.org/melodic/api/sensor_msgs/html/msg/Image.html)

- Control and Publish any value inside Blender using [std_msgs/Float64](https://docs.ros.org/api/std_msgs/html/msg/Float64.html) and [std_msgs/Int64](https://docs.ros.org/api/std_msgs/html/msg/Int64.html)

- Save Image sequence to chosen file path

- Adjustable Publish Rate


## Known Issues
- Don't Subscribe and Publish to the same topic - **Blender WILL CRASHES!!**

**NOTE: everything in "/external" is a direct copy from ROS repositories, Only included to avoid import errors.**
