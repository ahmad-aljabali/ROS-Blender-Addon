#import msg types here
from ROS_addon.external.std_msgs.msg import Int64, Float64

#call msgs creation functions by msg type here
def driver_pub(self):
    for driver in self.pub_drivers:
        if driver.message_type == 'Int64':
            msg = Int64(int(driver.value))
        if driver.message_type == 'Float64':
            msg = Float64(float(driver.value))

        self.publishers[driver.topic].publish(msg)

#define msgs creation functions here
