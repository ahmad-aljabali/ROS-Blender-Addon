import bpy

bpy.types.Scene.anonymous_node_bool = bpy.props.BoolProperty(default=False)
bpy.types.Scene.node_name = bpy.props.StringProperty(name="node_name", default="blender")
bpy.types.Scene.publish_rate = bpy.props.IntProperty(default=60, min=1, soft_max=200)


class ROS_PT_general_settings(bpy.types.Panel):
    bl_idname = "ROS_PT_general_settings"
    bl_label = "General Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ROS Bridge"


    def draw(self, context):
        layout = self.layout
        col = layout.column()
        if context.scene.ros_run_bool == False:
            col.label(text='Publish Rate')
            col.prop(context.scene, 'publish_rate', text='')
            col.label(text='View Lock:')
            row = col.row()
            row.label(text='Lock to Object')
            row.prop(context.space_data, 'lock_object', text='')
            col.prop(context.space_data, 'lock_camera', text='Lock Camera to View')
            col.operator('view3d.view_lock_clear', text='Clear View Lock')
        elif context.scene.ros_run_bool == True:
            layout.label(text="STOP to change settings")
