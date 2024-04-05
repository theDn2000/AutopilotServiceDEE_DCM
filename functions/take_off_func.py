import threading
import time
from pymavlink import mavutil



# Take off main function
def takeOff_MAVLINK(self, aTargetAltitude):
    
    mode = 'GUIDED'

    # Check if mode is available
    if mode not in self.vehicle.mode_mapping():
        print('Unknown mode : {}'.format(mode))
        print('Try:', list(self.vehicle.mode_mapping().keys()))

    # Get mode ID
    
    mode_id = self.vehicle.mode_mapping()[mode]
    self.vehicle.mav.set_mode_send(
        self.vehicle.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    arm_msg = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    print('- Autopilot Service: Mode changed to GUIDED')

    self.state = 'takingOff'
    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, aTargetAltitude)

    while True:
        if self.alt >= aTargetAltitude * 0.95:
            break
        time.sleep(1)
    self.state = "flying"

    # Enable flying trigger
    self.flying_trigger()
    print("Vehicle flying")

# Take off trigger function (for blocking and non-blocking)
def take_off(self,aTargetAltitude, blocking):
    if blocking:
        takeOff_MAVLINK(self, aTargetAltitude, True)
    else:
        t = threading.Thread(target=self.takeOff_MAVLINK, args=[aTargetAltitude])
        t.start()






 