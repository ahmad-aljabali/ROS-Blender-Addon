import bpy

class ROS_OT_stop(bpy.types.Operator):
    bl_idname = "ros.stop"
    bl_label = "stop operator"

    def execute(self, context):
        context.scene.ros_run_bool = False
        return {'FINISHED'}
