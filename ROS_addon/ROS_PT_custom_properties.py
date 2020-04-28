import bpy

class CustomPropertyItem(bpy.types.PropertyGroup):
    property: bpy.props.StringProperty(name="Property", default="")
    topic: bpy.props.StringProperty(name="Topic", default="")
    message_type: bpy.props.EnumProperty(name="Message Type", items = [("Float64", "Float64", "", 1), ("Int64", "Int64", "", 2)],
                                                             description="Message type used by ROS")
    mode_type: bpy.props.EnumProperty(items = [("subscriber", "Subscriber", "", 1),("publisher", "Publisher", "", 2)],
                                                         description="Mode for ROS topic")
class CustomPropertyList(bpy.types.PropertyGroup):
    items: bpy.props.CollectionProperty(type=CustomPropertyItem, name="Properties")
    active_item: bpy.props.IntProperty(name="Active Propertie", default=-1)
    val_hold: bpy.props.FloatProperty(name="Active Propertie", default=-1)


class ROS_UL_custom_properties(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        row = layout.row()
        row.prop(item, "property", text="")
        row.prop(item, "topic", text="")
        row.prop(item, "message_type",text="")
        row.prop(item, "mode_type",text="")

class ROS_PT_custom_properties(bpy.types.Panel):
    bl_idname = "ROS_PT_custom_properties"
    bl_label = "Custom Properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ROS Bridge"

    def draw(self, context):
        layout = self.layout
        list = context.scene.ros_properties_list

        if context.scene.ros_run_bool == False:
            row = layout.row()
            row.label(text='Property')
            row.label(text='Topic')
            row.label(text='Message Type')
            row.label(text='Type')

            layout.template_list(
                "ROS_UL_custom_properties",
                "custom_properties",
                list,
                "items",
                list,
                "active_item",
                type='DEFAULT'
            )

            row = layout.row(align=True)
            row.operator("ros.add_custom_property", icon='PLUS')
            row.operator("ros.del_custom_property", icon='CANCEL')

        elif context.scene.ros_run_bool == True:
            layout.label(text="STOP to change settings")

class ROS_OT_add_custom_property(bpy.types.Operator):
    bl_idname = "ros.add_custom_property"
    bl_label = "Add Property"

    def execute(self, context):
        list = context.scene.ros_properties_list
        list.items.add()
        list.active_item = len(list.items) - 1
        return {'FINISHED'}

class ROS_OT_del_custom_property(bpy.types.Operator):
    bl_idname = "ros.del_custom_property"
    bl_label = "Delete Property"

    @classmethod
    def poll(cls, context):
        return context.scene.ros_properties_list.active_item >= 0

    def execute(self, context):
        list = context.scene.ros_properties_list
        list.items.remove(list.active_item)
        list.active_item -= 1
        return {'FINISHED'}
