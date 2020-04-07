import bpy

bpy.types.Scene.ros_run_bool = bpy.props.BoolProperty(default=False)

class ROS_PT_run(bpy.types.Panel):
    bl_idname = "ROS_PT_run"
    bl_label = "Run"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ROS Bridge"


    def draw(self, context):
        layout = self.layout
        if bpy.context.scene.ros_run_bool == False:
            layout.operator("ros.run", text="START")
        elif bpy.context.scene.ros_run_bool == True:
            layout.operator("ros.stop", text="STOP")
