import threading
import dronekit
import time
from dronekit import connect, Command, VehicleMode

from AutopilotServiceDEE_DCM.functions_v0 import variables
import AutopilotServiceDEE_DCM.AutopilotService

def take_off_trigger():

    print(AutopilotServiceDEE_DCM.functions_v0.variables.state)
    w = threading.Thread(target=take_off_v0, args=[5, True])
    w.start()
    w.join()

def take_off_v0(a_target_altitude, manualControl):
    global state
    global vehicle
    AutopilotServiceDEE_DCM.functions_v0.variables.state = 'takingOff'
    AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.simple_takeoff(a_target_altitude)
    while True:
        print(" Altitude: ", AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.location.global_relative_frame.alt >= a_target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

    AutopilotServiceDEE_DCM.functions_v0.variables.state = 'flying'


