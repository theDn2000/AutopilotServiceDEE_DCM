import threading
import dronekit
import time

import AutopilotServiceDEE_DCM.AutopilotService


def returning_trigger():
    AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.mode = dronekit.VehicleMode("RTL")
    AutopilotServiceDEE_DCM.functions_v0.variables.state = 'returningHome'
    AutopilotServiceDEE_DCM.functions_v0.variables.direction = "RTL"
    AutopilotServiceDEE_DCM.functions_v0.variables.go = True
    w = threading.Thread(target=returning_v0)
    w.start()

def returning_v0():
    global sending_telemetry_info
    global external_client
    global internal_client
    global sending_topic
    global state

    # wait until the drone is at home
    while AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.armed:
        time.sleep(1)
    AutopilotServiceDEE_DCM.functions_v0.variables.state = 'onHearth'