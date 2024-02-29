import threading
import dronekit
import time
from pymavlink import mavutil


# Return to launch main function
def returnToLaunch_MAVLINK(self):
    mode = 'RTL'
    self.state = 'returningHome'
    self.going = True
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
    print('- Autopilot Service: Returning to launch')
    self.vehicle.motors_disarmed_wait()
    self.state = "onHearth"

# Return to launch trigger function (for blocking and non-blocking)
def return_to_launch(self, blocking):
    if blocking:
        returnToLaunch_MAVLINK(self)
    else:
        t = threading.Thread(target=self.returnToLaunch_MAVLINK)
        t.start()