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
from ROS_addon.ROS_PT_camera import ROS_PT_camera
from ROS_addon.ROS_PT_object_settings import ROS_PT_object_settings

def register():
    #register operators
    bpy.utils.register_class(ROS_OT_run)
    bpy.utils.register_class(ROS_OT_stop)

    #register UI elements
    bpy.utils.register_class(ROS_PT_run)
    bpy.utils.register_class(ROS_PT_camera)
    bpy.utils.register_class(ROS_PT_object_settings)

def unregister():
    #unregister operators
    bpy.utils.unregister_class(ROS_OT_run)
    bpy.utils.unregister_class(ROS_OT_stop)

    #unregister UI elements
    bpy.utils.unregister_class(ROS_PT_run)
    bpy.utils.unregister_class(ROS_PT_camera)
    bpy.utils.unregister_class(ROS_PT_object_settings)


if __name__ == "__main__":
    register()

