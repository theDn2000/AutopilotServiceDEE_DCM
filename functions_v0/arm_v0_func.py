import dronekit
import time
from pymavlink import mavutil


def arm_v0(self):
    print('arming')
    self.state = 'arming'

    """Arms vehicle and fly to aTargetAltitude"""
    print("Basic pre-arm checks")  # Don't try to arm until autopilot is ready
    self.vehicle.mode = dronekit.VehicleMode("GUIDED")
    while not self.vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    print("Arming motors")
    # Copter should arm in GUIDED mode

    self.vehicle.armed = True
    # Confirm vehicle armed before attempting to take off
    while not self.vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    print(" Armed")

    self.state = 'armed'
    return


def arm_MAVLINK(self):
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

    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    self.vehicle.motors_armed_wait()
    self.state = "armed"


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
