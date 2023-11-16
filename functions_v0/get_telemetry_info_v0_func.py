import json
import threading
import time
import dronekit # noqa: F401
from dronekit import connect, Command, VehicleMode # noqa: F401
from AutopilotServiceDEE_DCM.AutopilotService import state # noqa: F401

def get_telemetry_info (vehicle):
    global state
    telemetry_info = {
        'lat': vehicle.location.global_frame.lat,
        'lon': vehicle.location.global_frame.lon,
        'heading': vehicle.heading,
        'groundSpeed': vehicle.groundspeed,
        'altitude': vehicle.location.global_relative_frame.alt,
        'battery': vehicle.battery.level,
        'state': state
    }
    return telemetry_info