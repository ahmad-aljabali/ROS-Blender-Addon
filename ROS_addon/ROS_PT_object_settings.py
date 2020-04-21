import bpy

bpy.types.Object.topic = bpy.props.StringProperty(name="Topic")

bpy.types.Object.mode_type = bpy.props.EnumProperty(items = [("none", "None", "", 1),("subscriber", "Subscriber", "", 2),("publisher", "Publisher", "", 3)],
                                                         description="Mode for ROS topic")

bpy.types.Object.message_type = bpy.props.EnumProperty(items = [("Pose", "Pose", "", 1), ("Point", "Point", "", 2), ("Quaternion", "Quaternion", "", 3)],
                                                         description="Message type used by ROS")

class ROS_PT_object_settings(bpy.types.Panel):
    bl_idname = "ROS_PT_object_settings"
    bl_label = "Object Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ROS Bridge"

    def draw(self, context):
        layout = self.layout
        if bpy.context.scene.ros_run_bool == False:
            if not context.object or context.object.type == "CAMERA":
                layout.label(text="SLECT OBJECT")
            elif context.object.type != "CAMERA":
                layout.label(text="Mode:")
                row = layout.row()
                row.prop(context.object, "mode_type", expand=True)
                layout.label(text="Topic:")
                layout.prop(context.object, "topic", text="")
                layout.label(text="Message Type:")
                row = layout.row()
                row.prop(context.object, "message_type", expand=True)
        elif bpy.context.scene.ros_run_bool == True:
            layout.label(text="STOP to change settings")
