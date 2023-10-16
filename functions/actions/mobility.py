import json
import math

import threading
import paho.mqtt.client as mqtt
import time
import dronekit
from dronekit import connect, Command, VehicleMode
from paho.mqtt.client import ssl
from pymavlink import mavutil

# Import functions from the previous steps: init and processes
from ..processes import prepare_command


# Definition of the mobility functions that the drone is going to perform


# SET DIRECTION: Depending on the color recieved, the drone translate it to a certain direction. [NOTA: Debería ir a processes]
def set_direction(color):
    if color == 'blueS':
        return "North"
    elif color == "yellow":
        return "East"
    elif color == 'green':
        return "West"
    elif color == 'pink':
        return "South"
    elif color == 'purple':
        return "RTL"
    else:
        return "none"

# TAKE OFF: The drone takes off
