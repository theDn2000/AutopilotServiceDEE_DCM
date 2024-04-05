import dronekit
import time
from pymavlink import mavutil
import threading


# Arm maiun function
def arm_MAVLINK(self):

    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    self.vehicle.motors_armed_wait()
    self.state = "armed"

# Arm trigger function (for blocking and non-blocking)
def arm(self, blocking):
    if blocking:
        arm_MAVLINK(self)
    else:
        t = threading.Thread(target=arm_MAVLINK, args=(self,))
        t.start()


# Dev:
def armed_change(self):
    print('cambio a ', )
    if self.vehicle.armed:
        self.state = 'armed'
    else:
        self.state = 'disarmed'

    print('cambio a ', self.state)

def disarm(self):
    self.vehicle.armed = False
    while self.vehicle.armed:
        time.sleep(1)
    self.state = 'disarmed'
