import threading
import time
from pymavlink import mavutil



# Take off main function
def takeOff_MAVLINK(self, aTargetAltitude):
    self.state = 'takingOff'
    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, aTargetAltitude)

    while True:
        if self.alt >= aTargetAltitude * 0.95:
            break
        time.sleep(1)
    self.state = "flying"

# Take off trigger function (for blocking and non-blocking)
def take_off(self,aTargetAltitude, blocking):
    if blocking:
        takeOff_MAVLINK(self, aTargetAltitude, True)
    else:
        t = threading.Thread(target=self.takeOff_MAVLINK, args=[aTargetAltitude])
        t.start()






 