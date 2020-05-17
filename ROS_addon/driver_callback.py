#import msg types here
from ROS_addon.external.std_msgs.msg import Int64, Float64


#call call_back functions by msg type here
def driver_callback(msg, driver=None):
    if driver.message_type in {'Int64', 'Float64'}:
        driver.value = msg.data

#define msgs call_back functions here
