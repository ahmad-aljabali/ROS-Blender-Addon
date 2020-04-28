bl_info = {
    "name": "ROS add-on",
    "description": "addon designed to easliy connect blender to ROS for visualisation & VR Demos.",
    "author": "Ahmad Kutada Aljabali",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "support": "COMMUNITY",
    "category": "Development"
}

import bpy

from ROS_addon.ROS_OT_run import ROS_OT_run
from ROS_addon.ROS_OT_stop import ROS_OT_stop
from ROS_addon.ROS_PT_run import ROS_PT_run
from ROS_addon.ROS_PT_general_settings import ROS_PT_general_settings
from ROS_addon.ROS_PT_camera_settings import ROS_PT_camera_settings
from ROS_addon.ROS_PT_object_settings import ROS_PT_object_settings
from ROS_addon.ROS_PT_custom_properties import CustomPropertyItem, CustomPropertyList, ROS_UL_custom_properties, ROS_PT_custom_properties, ROS_OT_add_custom_property, ROS_OT_del_custom_property

classes = (
    ROS_OT_run,
    ROS_OT_stop,
    ROS_PT_run,
    ROS_PT_general_settings,
    ROS_PT_camera_settings,
    ROS_PT_object_settings,
    CustomPropertyItem,
    CustomPropertyList,
    ROS_UL_custom_properties,
    ROS_PT_custom_properties,
    ROS_OT_add_custom_property,
    ROS_OT_del_custom_property,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.ros_properties_list = bpy.props.PointerProperty(type=CustomPropertyList)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.ros_properties_list

if __name__ == "__main__":
    register()
