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

from AutopilotServiceDEE_DCM.functions_v0 import variables
import AutopilotServiceDEE_DCM.AutopilotService


def goto_v0(lat, lon, internal_client, external_client, sending_topic):
    global vehicle
    global state

    distanceThreshold = 1
    altitude = 6
    origin = sending_topic.split('/')[1]
    AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.mode = VehicleMode("GUIDED")

    destinationPoint = dronekit.LocationGlobalRelative(float(lat), float(lon), altitude)
    AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.simple_goto(destinationPoint, groundspeed=3)

    currentLocation = AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.location.global_frame
    dist = distanceInMeters(destinationPoint, currentLocation)

    while dist > distanceThreshold:
        time.sleep(0.25)
        currentLocation = AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.location.global_frame
        dist = distanceInMeters(destinationPoint, currentLocation)
    print('reached')
    destination_coordinates = {
        'lat': currentLocation.lat,
        'lon': currentLocation.lon
    }

    external_client.publish(sending_topic + "/destinationPointReached", json.dumps(destination_coordinates))
    AutopilotServiceDEE_DCM.functions_v0.variables.reaching_waypoint = False
    print("Destination reached, message published")


def distanceInMeters(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5
