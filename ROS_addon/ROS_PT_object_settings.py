import bpy

bpy.types.Object.topic = bpy.props.StringProperty(name="Topic")

bpy.types.Object.mode_type = bpy.props.EnumProperty(items = [("none", "None", "", 1),("subscriber", "Subscriber", "", 2),("publisher", "Publisher", "", 3)],
                                                         description="Mode for ROS topic")

bpy.types.Object.message_type = bpy.props.EnumProperty(items = [("Point", "Point", "", 1),("Pose", "Pose", "", 2)],
                                                         description="Message type used by ROS")

class ROS_PT_object_settings(bpy.types.Panel):
    bl_idname = "ROS_PT_object_settings"
    bl_label = "Object Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ROS Bridge"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        if bpy.context.scene.ros_run_bool == False:
            if not context.object or context.object.type == "CAMERA":
                layout.label(text="SLECT OBJECT")
            elif context.object.type != "CAMERA":
                col.label(text="Mode:")
                col.prop(context.object, "mode_type", text="")
                col.label(text="Topic:")
                col.prop(context.object, "topic", text="")
                col.label(text="Message Type:")
                col.prop(context.object, "message_type", text="")
        elif bpy.context.scene.ros_run_bool == True:
            layout.label(text="STOP to change settings")
