#import msg types here
from ROS_addon.external.geometry_msgs.msg import Point, Quaternion, Pose

#call msgs creation functions by msg type here
def object_pub(self):
    for object in self.pub_objects:
        if object.message_type == 'Point':
            msg = point_msg(object)
        if object.message_type == 'Quaternion':
            msg=quaternion_msg(object)
        if object.message_type == 'Pose':
            msg = Pose()
            msg.position = point_msg(object)
            msg.orientation = quaternion_msg(object)

        self.publishers[object.topic].publish(msg)

#define msgs creation functions here
def point_msg(object):
    msg = Point()
    msg.x, msg.y, msg.z = object.location.x, object.location.y, object.location.z
    return msg

def quaternion_msg(object):
    msg = Quaternion()
    msg.w, msg.x, msg.y, msg.z = object.rotation_quaternion.w, object.rotation_quaternion.x, object.rotation_quaternion.y, object.rotation_quaternion.z
    return msg
