import time
from pymavlink import mavutil
import threading


# Arm main function
def change_altitude(self, altitude, climb_rate):
    self.going = True
    self.direction = "changingAltitude"
    # Change the altitude of the vehicle while flying
    msg = self.vehicle.mav.command_long_encode(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_CONDITION_CHANGE_ALT, 0, int(altitude), 0, 0, 0, 0, 0, 0)
    self.vehicle.mav.send(msg)
    self.state = "changingAltitude"
    # Wait for the vehicle to reach the desired altitude [absolut value of the difference between the current altitude and the desired altitude is less than 0.5 meters]
    while abs(self.alt - altitude) > 0.5:
        time.sleep(0.1)
    self.going = False
    self.direction = "stop"
    # Return the state to flying
    self.state = "flying"
    # Execute the flying function again
    self.flying_trigger()
    



# Arm trigger function (for blocking and non-blocking)
def change_altitude_trigger(self, altitude, climb_rate, blocking):
    if blocking:
        change_altitude(self)
    else:
        t = threading.Thread(target=change_altitude, args=(self, altitude, climb_rate))
        t.start()
