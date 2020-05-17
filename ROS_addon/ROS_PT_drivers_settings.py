import bpy

class driver_item(bpy.types.PropertyGroup):
    value: bpy.props.FloatProperty(name="Value", default=0)
    topic: bpy.props.StringProperty(name="Topic", default="")
    message_type: bpy.props.EnumProperty(name="Message Type", items = [("Float64", "Float64", "", 1), ("Int64", "Int64", "", 2)],
                                                             description="Message type used by ROS")
    mode_type: bpy.props.EnumProperty(items = [("subscriber", "Subscriber", "", 1),("publisher", "Publisher", "", 2)],
                                                         description="Mode for ROS topic")
class drivers_list(bpy.types.PropertyGroup):
    items: bpy.props.CollectionProperty(type=driver_item, name="Drivers")
    active_item: bpy.props.IntProperty(name="Active Driver", default=-1)

class ROS_UL_drivers(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        row = layout.row()
        row.prop(item, "value", text="")
        row.prop(item, "topic", text="")
        row.prop(item, "message_type",text="")
        row.prop(item, "mode_type",text="")

class ROS_PT_drivers_settings(bpy.types.Panel):
    bl_idname = "ROS_PT_drivers_settings"
    bl_label = "Drivers Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ROS Bridge"

    def draw(self, context):
        layout = self.layout
        list = context.scene.ros_drivers_list

        if context.scene.ros_run_bool == False:
            row = layout.row()
            row.label(text='Driver')
            row.label(text='Topic')
            row.label(text='Message Type')
            row.label(text='Type')

            layout.template_list(
                "ROS_UL_drivers",
                "drivers",
                list,
                "items",
                list,
                "active_item",
                type='DEFAULT'
            )

            row = layout.row(align=True)
            row.operator("ros.add_driver", icon='PLUS')
            row.operator("ros.del_driver", icon='CANCEL')

        elif context.scene.ros_run_bool == True:
            layout.label(text="STOP to change settings")

class ROS_OT_add_driver(bpy.types.Operator):
    bl_idname = "ros.add_driver"
    bl_label = "Add Driver"

    def execute(self, context):
        list = context.scene.ros_drivers_list
        list.items.add()
        list.active_item = len(list.items) - 1
        return {'FINISHED'}

class ROS_OT_del_driver(bpy.types.Operator):
    bl_idname = "ros.del_driver"
    bl_label = "Delete Driver"

    @classmethod
    def poll(cls, context):
        return context.scene.ros_drivers_list.active_item >= 0

    def execute(self, context):
        list = context.scene.ros_drivers_list
        list.items.remove(list.active_item)
        list.active_item -= 1
        return {'FINISHED'}
