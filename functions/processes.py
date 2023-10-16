import json
import math

import threading
import paho.mqtt.client as mqtt
import time
import dronekit
from dronekit import connect, Command, VehicleMode
from paho.mqtt.client import ssl
from pymavlink import mavutil

# Definition of the functions describing processes


# PREPARE COMMAND: Prepares a command to move vehicle in direction based on specified velocity vectors
def prepare_command(velocity_x, velocity_y, velocity_z, vehicle):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,  # time_boot_ms (not used)
        0,
        0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0,
        0,
        0,  # x, y, z positions (not used)
        velocity_x,
        velocity_y,
        velocity_z,  # x, y, z velocity in m/s
        0,
        0,
        0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0,
        0,
    )  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    return msg

# GET TELEMETRY INFO: Gets the info of the vehicle
def get_telemetry_info(vehicle, state):
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

# SEND TELEMETRY INFO: Sends the info of the vehicle
def send_telemetry_info(vehicle, state, external_client, sending_telemetry_info, sending_topic):

    while sending_telemetry_info:
        external_client.publish(sending_topic + "/telemetryInfo", json.dumps(get_telemetry_info(vehicle, state)))
        time.sleep(0.25)