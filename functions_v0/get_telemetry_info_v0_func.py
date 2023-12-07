import dronekit  # noqa: F401
from dronekit import connect, Command, VehicleMode  # noqa: F401

import AutopilotServiceDEE_DCM.AutopilotService

def get_telemetry_info():
    global state
    global vehicle
    telemetry_info = {
        'lat': AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.location.global_frame.lat,
        'lon': AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.location.global_frame.lon,
        'heading': AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.heading,
        'groundSpeed': AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.groundspeed,
        'altitude': AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.location.global_relative_frame.alt,
        'battery': AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.battery.level,
        'state': AutopilotServiceDEE_DCM.functions_v0.variables.state
    }
    return telemetry_info
