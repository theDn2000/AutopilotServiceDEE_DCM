import dronekit
import time


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
