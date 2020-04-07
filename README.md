# ROS-Blender-Addon
Add-on to use Blender for visualization with ROS (Robot Operating System).

Download ROS_addon.zip to install it in blender.

![Screenshot](https://github.com/ahmad-aljabali/ROS-Blender-Addon/blob/master/ROS_addon%20screenshot.png)


## Features
- Control objects Location using [geometry_msgs/Point](https://docs.ros.org/api/geometry_msgs/html/msg/Point.html)

- Control objects Location & Rotation using [geometry_msgs/Pose](https://docs.ros.org/api/geometry_msgs/html/msg/Pose.html)

- Publish objects Location using [geometry_msgs/Point](https://docs.ros.org/api/geometry_msgs/html/msg/Point.html)

- Publish objects Location & Rotation using [geometry_msgs/Pose](https://docs.ros.org/api/geometry_msgs/html/msg/Pose.html)

- Save Image sequence to chosen file path


## Planed Improvements
### Short term:
#### UI:
- Lock view to object or camera

- Variable FPS for camera publishing and saving

- option to Define ROS node name
#### ROS:
- Add rotation message [geometry_msgs/Quaternion](https://docs.ros.org/api/geometry_msgs/html/msg/Quaternion.html)

- Implement camera Publishing
### Long term:
#### UI:
- Option to Lock Axis (i.e select X-position is not effected by message)
#### ROS:
- Add support for velocity, acceleration etc.. messages

- Add multi-cam\stereo support

- Add generic float and int messages to control any value inside Blender 



## Known Issues
- Don't Subscribe and Publish to the same topic - **Blender WILL CRASHES!!**
- Camera publishing is not yet implemented but SAVE IS functional.


**NOTE: (geometry_msgs) and (sensor_msgs) are included In the zip file for user convenience, I don't own them they're a direct copy from ROS repositories.**
