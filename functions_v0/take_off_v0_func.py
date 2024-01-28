import threading
import time
from pymavlink import mavutil


def take_off_trigger(self):
    w = threading.Thread(target=self.takeOff_MAVLINK, args=[5, True])
    w.start()
    w.join()


def take_off_v0(self, a_target_altitude, manualControl):
    self.state = 'takingOff'
    self.vehicle.simple_takeoff(a_target_altitude)
    while True:
        print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if self.vehicle.location.global_relative_frame.alt >= a_target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

    self.state = 'flying'

def takeOff_MAVLINK(self, aTargetAltitude, manualControl):
    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, aTargetAltitude)

    while True:
        if self.alt >= aTargetAltitude * 0.95:
            break
        time.sleep(1)
    self.state = "flying"
