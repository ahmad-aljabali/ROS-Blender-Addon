import bpy
import rospy
from geometry_msgs.msg import Point, Quaternion, Pose
from sensor_msgs.msg import Image
from functools import partial
import time


class ROS_OT_run(bpy.types.Operator):
    bl_idname = "ros.run"
    bl_label = "subscribe operator"

    msgs = {'Point':Point, 'Quaternion':Quaternion,'Pose':Pose}

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

        wm = context.window_manager
        wm.modal_handler_add(self)
        self._timer = wm.event_timer_add(1/context.scene.publish_rate, window=context.window)


        if rospy.client.rosgraph.is_master_online() == True:
            rospy.init_node('blender', anonymous=True)
            if context.scene.ros_video_out_bool==True and context.scene.camera.topic != '':
                self.cam_pub = rospy.Publisher(context.scene.camera.topic, Image, queue_size=10)
            for object in bpy.data.objects:
                if object.mode_type == 'subscriber' and object.topic != '':
                    object.rotation_mode = 'QUATERNION'
                    self.subscribers.append(rospy.Subscriber(object.topic, self.msgs[object.message_type], partial(self.callback,object=object)))
                if object.mode_type == 'publisher' and object.topic != '':
                    object.rotation_mode = 'QUATERNION'
                    self.pub_objects.append(object.name_full)
                    self.publishers[object.name_full] = rospy.Publisher(object.topic, self.msgs[object.message_type], queue_size=1)



        # switch on nodes
        context.scene.use_nodes = True
        tree = context.scene.node_tree
        links = tree.links

        # clear default nodes
        for n in tree.nodes:
            tree.nodes.remove(n)

        # create input render layer node
        rl = tree.nodes.new('CompositorNodeRLayers')
        rl.location = 185,285

        # create output node
        v = tree.nodes.new('CompositorNodeViewer')
        v.location = 750,210
        v.use_alpha = False

        links.new(rl.outputs[0], v.inputs[0])  # link Image output to Viewer input

        return {'RUNNING_MODAL'}


    def pointCB(self, msg, object):
        object.location.x = msg.x
        object.location.y = msg.y
        object.location.z = msg.z

    def quaternionCB(self, msg, object):
        object.rotation_quaternion.w = msg.w
        object.rotation_quaternion.x = msg.x
        object.rotation_quaternion.y = msg.y
        object.rotation_quaternion.z = msg.z

    def callback(self, msg, object=None):
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

    def camera_pub(self, context):
        bpy.ops.render.render()
        if context.scene.ros_video_out_bool==True and context.scene.camera.topic!='':
            pixels = bpy.data.images['Viewer Node'].pixels

        if context.scene.ros_video_save_bool == True and context.scene.camera.save_path != '':
            bpy.data.images['Render Result'].save_render(filepath=context.scene.camera.save_path +"/"+str(time.time_ns())+"."+context.scene.render.image_settings.file_format)
