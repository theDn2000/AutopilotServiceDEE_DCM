import json
import math

import threading
import paho.mqtt.client as mqtt
import time
import dronekit
from dronekit import connect, Command, VehicleMode
from paho.mqtt.client import ssl
from pymavlink import mavutil
import dronekit  # noqa: F401
from dronekit import connect, Command, VehicleMode  # noqa: F401

import AutopilotServiceDEE_DCM.AutopilotService

def get_telemetry_info():
    global state
    global vehicle
    print(AutopilotServiceDEE_DCM.functions_v0.variables.state)
    telemetry_info = {
        'lat': AutopilotServiceDEE_DCM.AutopilotService.vehicle.location.global_frame.lat,
        'lon': AutopilotServiceDEE_DCM.AutopilotService.vehicle.location.global_frame.lon,
        'heading': AutopilotServiceDEE_DCM.AutopilotService.vehicle.heading,
        'groundSpeed': AutopilotServiceDEE_DCM.AutopilotService.vehicle.groundspeed,
        'altitude': AutopilotServiceDEE_DCM.AutopilotService.vehicle.location.global_relative_frame.alt,
        'battery': AutopilotServiceDEE_DCM.AutopilotService.vehicle.battery.level,
        'state': AutopilotServiceDEE_DCM.functions_v0.variables.state
    }
    return telemetry_info
