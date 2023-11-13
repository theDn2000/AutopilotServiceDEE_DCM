import json
import math

from queue import Queue
import threading
import paho.mqtt.client as mqtt
import time
import dronekit
from dronekit import connect, Command, VehicleMode
from paho.mqtt.client import ssl
from pymavlink import mavutil

global sending_telemetry_info
global state
global vehicle

# Define lock to share variables between threads:
lock = threading.Lock()


# Definition of the functions describing processes


# PREPARE COMMAND: Prepares a command to move vehicle in direction based on specified velocity vectors
def prepare_command(velocity_x, velocity_y, velocity_z):
    global vehicle
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
def get_telemetry_info(vehicle):
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
def send_telemetry_info(vehicle_init, external_client, sending_topic):
    global vehicle
    vehicle = vehicle_init
    while sending_telemetry_info:
        external_client.publish(sending_topic + "/telemetryInfo", json.dumps(get_telemetry_info(vehicle)))
        time.sleep(0.25)


# CHANGE STATE: Changes the actual state of the vehicle
def change_state(newstate):
    global state
    state = newstate


# GET STATE: Gets the state of the vehicle
def get_state():
    return state


def change_vehicle(newvehicle):
    global vehicle
    vehicle = newvehicle


def get_vehicle():
    return vehicle
