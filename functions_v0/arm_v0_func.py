import threading
import dronekit
import time
from dronekit import connect, Command, VehicleMode

import AutopilotServiceDEE_DCM.AutopilotService


def arm_v0():
    global vehicle

    print('arming')
    AutopilotServiceDEE_DCM.AutopilotService.state = 'arming'

    """Arms vehicle and fly to aTargetAltitude"""
    print("Basic pre-arm checks")  # Don't try to arm until autopilot is ready
    AutopilotServiceDEE_DCM.AutopilotService.vehicle.mode = dronekit.VehicleMode("GUIDED")
    while not AutopilotServiceDEE_DCM.AutopilotService.vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    print("Arming motors")
    # Copter should arm in GUIDED mode

    AutopilotServiceDEE_DCM.AutopilotService.vehicle.armed = True
    # Confirm vehicle armed before attempting to take off
    while not AutopilotServiceDEE_DCM.AutopilotService.vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    print(" Armed")

    AutopilotServiceDEE_DCM.AutopilotService.state = 'armed'