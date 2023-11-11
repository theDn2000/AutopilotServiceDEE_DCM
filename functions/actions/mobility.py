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

# Global variables:
global go
global direction


# Definition of the mobility functions that the drone is going to perform

# TAKE OFF: The vehicle takes off
def take_off(a_target_altitude, manualControl, vehicle, state):
    vehicle.simple_takeoff(a_target_altitude)
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= a_target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

    state = 'flying'
    if manualControl:
        w = threading.Thread(target=flying, args=[vehicle])
        w.start()


# FLYING: The vehicle flights thowards the stablished directon
def flying(vehicle):
    speed = 1
    end = False
    cmd = prepare_command(0, 0, 0, vehicle)  # stop
    while not end:
        go = False
        while not go:
            vehicle.send_mavlink(cmd)
            time.sleep(1)
        # a new go command has been received. Check direction
        print('salgo del bucle por ', direction)
        if direction == "North":
            cmd = prepare_command(speed, 0, 0, vehicle)  # NORTH
        if direction == "South":
            cmd = prepare_command(-speed, 0, 0, vehicle)  # SOUTH
        if direction == "East":
            cmd = prepare_command(0, speed, 0, vehicle)  # EAST
        if direction == "West":
            cmd = prepare_command(0, -speed, 0, vehicle)  # WEST
        if direction == "NorthWest":
            cmd = prepare_command(speed, -speed, 0, vehicle)  # NORTHWEST
        if direction == "NorthEast":
            cmd = prepare_command(speed, speed, 0, vehicle)  # NORTHEST
        if direction == "SouthWest":
            cmd = prepare_command(-speed, -speed, 0, vehicle)  # SOUTHWEST
        if direction == "SouthEast":
            cmd = prepare_command(-speed, speed, 0, vehicle)  # SOUTHEST
        if direction == "Stop":
            cmd = prepare_command(0, 0, 0, vehicle)  # STOP
        if direction == "RTL":
            end = True

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
