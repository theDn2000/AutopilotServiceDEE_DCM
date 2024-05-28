import time
from pymavlink import mavutil
import threading


# Arm main function
def change_altitude(self, altitude, climb_rate):
    self.reaching_waypoint = True
    # Change the altitude of the vehicle while flying
    self.vehicle.mav.send(
        mavutil.mavlink.MAVLink_set_position_target_global_int_message(1, self.vehicle.target_system,
                                                                       self.vehicle.target_component,
                                                                       mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                                                       int(0b110111111000), int(self.lat * 10 ** 7),
                                                                       int(self.lon * 10 ** 7), altitude, 0, 0, 0, 0, 0, 0, 0,
                                                                       0))
    self.state = "changingAltitude"
    # Wait for the vehicle to reach the desired altitude [absolut value of the difference between the current altitude and the desired altitude is less than 0.5 meters]
    while abs(self.alt - altitude) > 0.5:
        time.sleep(0.1)
    # The vehicle has reached the desired altitude
    self.reaching_waypoint = False
    # Execute the flying function again
    self.state = "flying"
    self.flying_trigger()
    



# Arm trigger function (for blocking and non-blocking)
def change_altitude_trigger(self, altitude, climb_rate, blocking):
    if blocking:
        change_altitude(self)
    else:
        t = threading.Thread(target=change_altitude, args=(self, altitude, climb_rate))
        t.start()
