import bpy

bpy.types.Object.topic = bpy.props.StringProperty(name="Topic")
bpy.types.Object.active_pos_axis = bpy.props.BoolVectorProperty(name='Position Axis', default=(True,True,True), subtype='XYZ')
bpy.types.Object.active_rot_axis = bpy.props.BoolVectorProperty(name='Rotation Axis', default=(True,True,True), subtype='XYZ')
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
        col = layout.column()
        if bpy.context.scene.ros_run_bool == False:
            if not context.object or context.object.type == "CAMERA":
                col.label(text="SLECT OBJECT")
            elif context.object.type != "CAMERA":
                col.label(text="Mode:")
                row = col.row()
                row.prop(context.object, "mode_type", expand=True)
                col.label(text="Topic:")
                col.prop(context.object, "topic", text="")
                col.label(text="Message Type:")
                row = col.row()
                row.prop(context.object, "message_type", expand=True)
                if context.object.mode_type == 'subscriber':
                    if context.object.message_type in ('Pose','Point'):
                        col.label(text="Position Axis:")
                        row = col.row()
                        row.prop(context.object, "active_pos_axis", text='')
                    if context.object.message_type in ('Pose','Quaternion'):
                        col.label(text="Rotation Axis:")
                        row = col.row()
                        row.prop(context.object, "active_rot_axis", text='')
        elif bpy.context.scene.ros_run_bool == True:
            layout.label(text="STOP to change settings")
