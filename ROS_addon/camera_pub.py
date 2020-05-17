import bpy
import cv2
import time

def camera_pub(self, context):
    bpy.ops.render.render()
    save_path = ""
    if context.scene.ros_video_save_bool == True and context.scene.camera.save_path != '':
        save_path = context.scene.camera.save_path +"/"+str(time.time_ns())+"."+context.scene.render.image_settings.file_format
        bpy.data.images['Render Result'].save_render(filepath= save_path)
    else:
        save_path = "./tmp/render_result."+context.scene.render.image_settings.file_format
        bpy.data.images['Render Result'].save_render(filepath= save_path)

    if context.scene.ros_video_out_bool==True and context.scene.camera.topic!='':
        img = cv2.imread(save_path)
        self.cam_pub.publish(self.bridge.cv2_to_imgmsg(img, encoding="passthrough"))
