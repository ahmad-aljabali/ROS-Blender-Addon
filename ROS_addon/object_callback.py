#import msg types here
from ROS_addon.external.geometry_msgs.msg import Point, Quaternion, Pose

#call call_back functions by msg type here
def object_callback(msg, object=None):
    if object.message_type == 'Point':
        point_callback(msg,object)
    elif object.message_type == 'Quaternion':
        quaternion_callback(msg,object)
    elif object.message_type == 'Pose':
        point_callback(msg.position, object)
        quaternion_callback(msg.orientation, object)

#define msgs call_back functions here
def point_callback(msg, object):
    if object.active_pos_axis[0]:
        object.location[0] = msg.x
    if object.active_pos_axis[1]:
        object.location[1] = msg.y
    if object.active_pos_axis[2]:
        object.location[2] = msg.z

def quaternion_callback(msg, object):
    object.rotation_mode = 'XYZ'
    old_rotation = [None,None,None]
    (old_rotation[0],old_rotation[1],old_rotation[2]) = object.rotation_euler
    object.rotation_mode = 'QUATERNION'
    object.rotation_quaternion.w = msg.w
    object.rotation_quaternion.x = msg.x
    object.rotation_quaternion.y = msg.y
    object.rotation_quaternion.z = msg.z
    object.rotation_mode = 'XYZ'
    for i in (0,1,2):
        if not object.active_rot_axis[i]:
            object.rotation_euler[i] = old_rotation[i]
