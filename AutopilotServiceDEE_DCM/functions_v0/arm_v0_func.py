import threading
import dronekit
import time

import AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.AutopilotService


def arm_v0():
    global vehicle

    print('arming')
    AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.AutopilotService.state = 'arming'

    """Arms vehicle and fly to aTargetAltitude"""
    print("Basic pre-arm checks")  # Don't try to arm until autopilot is ready
    AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.mode = dronekit.VehicleMode("GUIDED")
    while not AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    print("Arming motors")
    # Copter should arm in GUIDED mode

    AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.armed = True
    # Confirm vehicle armed before attempting to take off
    while not AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    print(" Armed")

    AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.state = 'armed'
    return



def armed_change():
    global vehicle
    global state
    print('cambio a ', )
    if AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.armed:
        AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.state = 'armed'
    else:
        AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.state = 'disarmed'

    print('cambio a ', AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.state)

def disarm():
    AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.armed = False
    while AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.armed:
        time.sleep(1)
    AutopilotServiceDEE_DCM.AutopilotServiceDEE_DCM.functions_v0.variables.state = 'disarmed'
