import bpy
import rospy
from ROS_addon.external.geometry_msgs.msg import Point, Quaternion, Pose
from ROS_addon.external.sensor_msgs.msg import Image
from ROS_addon.external.std_msgs.msg import Int64, Float64
from ROS_addon.external.cv_bridge import CvBridge
import cv2
from functools import partial
import time

from ROS_addon.object_callback import object_callback
from ROS_addon.object_pub import object_pub

from ROS_addon.driver_callback import driver_callback
from ROS_addon.driver_pub import driver_pub


class ROS_OT_run(bpy.types.Operator):
    bl_idname = "ros.run"
    bl_label = "subscribe operator"

    msg_types = {'Point':Point, 'Quaternion':Quaternion,'Pose':Pose, 'Int64':Int64, 'Float64':Float64}

    def modal(self, context, event):
        if event.type == 'TIMER':
            if context.scene.ros_run_bool == False:
                wm = context.window_manager
                wm.event_timer_remove(self._timer)
                for sub in self.subscribers:
                    sub.unregister()
                return {'FINISHED'}
            else:
                object_pub(self)
                driver_pub(self)
                if context.scene.ros_video_out_bool==True or  context.scene.ros_video_save_bool==True:
                    self.camera_pub(context)
                return {'RUNNING_MODAL'}

        else:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        context.scene.ros_run_bool = True

        self.subscribers = []
        self.publishers = {}
        self.pub_objects = []
        self.pub_drivers = []
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
                    self.subscribers.append(rospy.Subscriber(object.topic, self.msg_types[object.message_type], partial(object_callback,object=object)))
                if object.mode_type == 'publisher' and object.topic != '':
                    object.rotation_mode = 'QUATERNION'
                    self.pub_objects.append(object)
                    self.publishers[object.topic] = rospy.Publisher(object.topic, self.msg_types[object.message_type], queue_size=1)

            for driver in bpy.context.scene.ros_drivers_list.items:
                if driver.mode_type == 'subscriber' and driver.topic != '':
                    self.subscribers.append(rospy.Subscriber(driver.topic, self.msg_types[driver.message_type], partial(driver_callback,driver=driver)))
                if driver.mode_type == 'publisher' and driver.topic != '':
                    self.pub_drivers.append(driver)
                    self.publishers[driver.topic] = rospy.Publisher(driver.topic, self.msg_types[driver.message_type], queue_size=1)

        return {'RUNNING_MODAL'}


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
