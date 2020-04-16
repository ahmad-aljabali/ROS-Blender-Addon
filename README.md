# ROS-Blender-Addon
Add-on to use Blender for visualization with ROS (Robot Operating System).

Download ROS_addon.zip to install it in blender.
## Install dependancies
```Shell
sudo apt install python3-rospy python3-opencv python3-cv-bridge
```

![Screenshot](https://github.com/ahmad-aljabali/ROS-Blender-Addon/blob/master/ROS_addon%20screenshot.png)


## Features
- Control and Publish objects Location using [geometry_msgs/Point](https://docs.ros.org/api/geometry_msgs/html/msg/Point.html)

- Control and Publish objects Rotation using [geometry_msgs/Quaternion](https://docs.ros.org/api/geometry_msgs/html/msg/Quaternion.html)

- Control and Publish objects Location & Rotation using [geometry_msgs/Pose](https://docs.ros.org/api/geometry_msgs/html/msg/Pose.html)

- Publish Rendered Image Stream using [sensor_msgs/Image](https://docs.ros.org/melodic/api/sensor_msgs/html/msg/Image.html)

- Save Image sequence to chosen file path

- Adjustable Publish Rate


## Planed Improvements
#### UI:
- Option to Lock Axis (i.e select X-position is not effected by message)
#### ROS:
- Add generic float and int messages to control any value inside Blender 

- Add support for velocity, acceleration etc.. messages

- Add multi-cam\stereo support


## Known Issues
- Don't Subscribe and Publish to the same topic - **Blender WILL CRASHES!!**

**NOTE: (geometry_msgs) and (sensor_msgs) are included In the zip file for user convenience, I don't own them they're a direct copy from ROS repositories.**
