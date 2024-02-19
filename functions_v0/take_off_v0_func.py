import threading
import time
from pymavlink import mavutil


def take_off_trigger(self):
    w = threading.Thread(target=self.takeOff_MAVLINK, args=[5, True])
    w.start()
    w.join()

def takeOff_MAVLINK(self, aTargetAltitude, manualControl):
    self.state = 'takingOff'
    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, aTargetAltitude)

    while True:
        if self.alt >= aTargetAltitude * 0.95:
            break
        time.sleep(1)
    self.state = "flying"
