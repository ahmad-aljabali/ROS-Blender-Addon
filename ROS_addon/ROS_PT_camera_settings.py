import bpy

bpy.types.Scene.ros_video_out_bool = bpy.props.BoolProperty(default=False)
bpy.types.Scene.ros_video_save_bool = bpy.props.BoolProperty(default=False)
bpy.types.Object.save_path = bpy.props.StringProperty(name="Save_path")


class ROS_PT_camera_settings(bpy.types.Panel):
    bl_idname = "ROS_PT_camera_settings"
    bl_label = "Camera Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ROS Bridge"


    def draw(self, context):
        layout = self.layout
        col = layout.column()
        if context.scene.ros_run_bool == False:
            col.label(text="Select Active Camera")
            col.prop(context.scene, 'camera', text="")
            col.prop(context.scene,'ros_video_out_bool', text="Publish Video to ROS")
            if context.scene.ros_video_out_bool == True:
                col.label(text="Topic:")
                col.prop(context.scene.camera, "topic", text="")
            col.prop(context.scene,'ros_video_save_bool', text="Save Frames to a Folder")
            if context.scene.ros_video_save_bool == True:
                col.label(text="Save Path")
                col.prop(context.scene.camera, "save_path", text="")
        elif context.scene.ros_run_bool == True:
            layout.label(text="STOP to change settings")
