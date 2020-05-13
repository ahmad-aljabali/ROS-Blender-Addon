import bpy
import rospy
from ROS_addon.external.geometry_msgs.msg import Point, Quaternion, Pose
from ROS_addon.external.sensor_msgs.msg import Image
from ROS_addon.external.std_msgs.msg import Int64, Float64
from ROS_addon.external.cv_bridge import CvBridge
import cv2
from functools import partial
import time


class ROS_OT_run(bpy.types.Operator):
    bl_idname = "ros.run"
    bl_label = "subscribe operator"

    msgs = {'Point':Point, 'Quaternion':Quaternion,'Pose':Pose, 'Int64':Int64, 'Float64':Float64}

    def modal(self, context, event):
        if event.type == 'TIMER':
            if context.scene.ros_run_bool == False:
                wm = context.window_manager
                wm.event_timer_remove(self._timer)
                for sub in self.subscribers:
                    sub.unregister()
                return {'FINISHED'}
            else:
                self.object_pub()
                self.prop_pub()
                if context.scene.ros_video_out_bool==True or  context.scene.ros_video_save_bool==True:
                    self.camera_pub(context)
                return {'RUNNING_MODAL'}

        elif event.type in {'MOUSEMOVE', 'LEFTMOUSE','MIDDLEMOUSE','WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        context.scene.ros_run_bool = True

        self.subscribers = []
        self.publishers = {}
        self.pub_objects = []
        self.pub_props = []
        self.bridge = CvBridge()

        wm = context.window_manager
        wm.modal_handler_add(self)
        self._timer = wm.event_timer_add(1/context.scene.publish_rate, window=context.window)


        if rospy.client.rosgraph.is_master_online() == True:
            rospy.init_node(context.scene.node_name, anonymous=context.scene.anonymous_node_bool)
            if context.scene.ros_video_out_bool==True and context.scene.camera.topic != '':
                self.cam_pub = rospy.Publisher(context.scene.camera.topic, Image, queue_size=10)
            for object in bpy.data.objects:
                if object.mode_type == 'subscriber' and object.topic != '':
                    object.rotation_mode = 'QUATERNION'
                    self.subscribers.append(rospy.Subscriber(object.topic, self.msgs[object.message_type], partial(self.object_callback,object=object)))
                if object.mode_type == 'publisher' and object.topic != '':
                    object.rotation_mode = 'QUATERNION'
                    self.pub_objects.append(object.name_full)
                    self.publishers[object.name_full] = rospy.Publisher(object.topic, self.msgs[object.message_type], queue_size=1)

            for prop in bpy.context.scene.ros_properties_list.items:
                if prop.mode_type == 'subscriber' and prop.topic != '':
                    self.subscribers.append(rospy.Subscriber(prop.topic, self.msgs[prop.message_type], partial(self.prop_callback,prop=prop)))
                if prop.mode_type == 'publisher' and prop.topic != '':
                    self.pub_props.append(prop)
                    self.publishers[prop.topic] = rospy.Publisher(prop.topic, self.msgs[prop.message_type], queue_size=1)

        return {'RUNNING_MODAL'}


    def pointCB(self, msg, object):
        if object.active_pos_axis[0]:
            object.location[0] = msg.x
        if object.active_pos_axis[1]:
            object.location[1] = msg.y
        if object.active_pos_axis[2]:
            object.location[2] = msg.z

    def quaternionCB(self, msg, object):
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


    def object_callback(self, msg, object=None):
        if object.message_type == 'Point':
            self.pointCB(msg,object)
        elif object.message_type == 'Quaternion':
            self.quaternionCB(msg,object)
        elif object.message_type == 'Pose':
            self.pointCB(msg.position, object)
            self.quaternionCB(msg.orientation, object)

    def pointMsg(self,object):
        msg = Point()
        msg.x, msg.y, msg.z = object.location.x, object.location.y, object.location.z
        return msg

    def quaternionMsg(self,object):
        msg = Quaternion()
        msg.w, msg.x, msg.y, msg.z = object.rotation_quaternion.w, object.rotation_quaternion.x, object.rotation_quaternion.y, object.rotation_quaternion.z
        return msg

    def object_pub(self):
        for name in self.pub_objects:
            object = bpy.data.objects[name]
            if object.message_type == 'Point':
                self.publishers[name].publish(self.pointMsg(object))
            if object.message_type == 'Quaternion':
                self.publishers[name].publish(self.quaternionMsg(object))
            if object.message_type == 'Pose':
                msg = Pose()
                msg.position = self.pointMsg(object)
                msg.orientation = self.quaternionMsg(object)
                self.publishers[name].publish(msg)

    def prop_callback(self, msg, prop=None):
        prop.value = msg.data

    def prop_pub(self):
        for prop in self.pub_props:
            if prop.message_type == 'Int64':
                print(int(prop.value))
                self.publishers[prop.topic].publish(Int64(int(prop.value)))
            if prop.message_type == 'Float64':
                print(float(val))
                self.publishers[prop.topic].publish(Float64(float(prop.value)))

    def camera_pub(self, context):
        bpy.ops.render.render()
        save_path = ""
        if context.scene.ros_video_save_bool == True and context.scene.camera.save_path != '':
            save_path = context.scene.camera.save_path +"/"+str(time.time_ns())+"."+context.scene.render.image_settings.file_format
            bpy.data.images['Render Result'].save_render(filepath= save_path)
        else:
            save_path = "./tmp/render_result."+context.scene.render.image_settings.file_format
            bpy.data.images['Render Result'].save_render(filepath= save_path)

        if context.scene.ros_video_out_bool==True and context.scene.camera.topic!='':
            img = cv2.imread(save_path)
            self.cam_pub.publish(self.bridge.cv2_to_imgmsg(img, encoding="passthrough"))
