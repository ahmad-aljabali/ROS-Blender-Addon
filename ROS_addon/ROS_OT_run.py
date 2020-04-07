import bpy
import rospy
from geometry_msgs.msg import Point, Pose
from sensor_msgs.msg import Image
from functools import partial
import time


class ROS_OT_run(bpy.types.Operator):
    bl_idname = "ros.run"
    bl_label = "subscribe operator"

    msgs = {'Point':Point, 'Pose':Pose}

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
        self._timer = wm.event_timer_add(1/120, window=context.window)


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



    def callback(self, msg, object=None):
        if object.message_type == 'Point':
            object.location.x = msg.x
            object.location.y = msg.y
            object.location.z = msg.z
        elif object.message_type == 'Pose':
            pass
            p = msg.position
            object.location.x = p.x
            object.location.y = p.y
            object.location.z = p.z
            o = msg.orientation
            object.rotation_quaternion.w = o.w
            object.rotation_quaternion.x = o.x
            object.rotation_quaternion.y = o.y
            object.rotation_quaternion.z = o.z


    def object_pub(self):
        for name in self.pub_objects:
            object = bpy.data.objects[name]
            if object.message_type == 'Point':
                msg = Point()
                msg.x, msg.y, msg.z = object.location.x, object.location.y, object.location.z
                self.publishers[name].publish(msg)
            if object.message_type == 'Pose':
                msg = Pose()
                p = msg.position
                p.x, p.y, p.z = object.location.x, object.location.y, object.location.z
                o = msg.orientation
                o.w, o.x, o.y, o.z = object.rotation_quaternion.w, object.rotation_quaternion.x, object.rotation_quaternion.y, object.rotation_quaternion.z

                self.publishers[name].publish(msg)

    def camera_pub(self, context):
        bpy.ops.render.render()
        if context.scene.ros_video_out_bool==True and context.scene.camera.topic!='':
            pixels = bpy.data.images['Viewer Node'].pixels

        if context.scene.ros_video_save_bool == True and context.scene.camera.save_path != '':
            bpy.data.images['Render Result'].save_render(filepath=context.scene.camera.save_path +"/"+str(time.time_ns())+"."+context.scene.render.image_settings.file_format)
