import threading
import time

import AutopilotServiceDEE_DCM.functions.processes
# Import functions from the previous steps: init and processes
from ..processes import prepare_command, change_state, change_vehicle, get_vehicle, lock

# Global variables:
global go
global direction


# Definition of the mobility functions that the drone is going to perform

# TAKE OFF: The vehicle takes off
def take_off(a_target_altitude, manualControl, vehicle):
    with lock:
        vehicle.simple_takeoff(a_target_altitude)
        while True:
            print(" Altitude: ", vehicle.location.global_relative_frame.alt)
            # Break and return from function just below target altitude.
            if vehicle.location.global_relative_frame.alt >= a_target_altitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)

        change_state('flying')


# FLYING: The vehicle flights thowards the stablished directon
def flying():
    speed = 1
    end = False
    cmd = prepare_command(0, 0, 0)  # stop
    while not end:
        go = False
        while not go:
            get_vehicle().send_mavlink(cmd)
            time.sleep(1)
        # a new go command has been received. Check direction
        print('salgo del bucle por ', direction)
        if direction == "North":
            cmd = prepare_command(speed, 0, 0)  # NORTH
        if direction == "South":
            cmd = prepare_command(-speed, 0, 0)  # SOUTH
        if direction == "East":
            cmd = prepare_command(0, speed, 0)  # EAST
        if direction == "West":
            cmd = prepare_command(0, -speed, 0)  # WEST
        if direction == "NorthWest":
            cmd = prepare_command(speed, -speed, 0)  # NORTHWEST
        if direction == "NorthEast":
            cmd = prepare_command(speed, speed, 0)  # NORTHEST
        if direction == "SouthWest":
            cmd = prepare_command(-speed, -speed, 0)  # SOUTHWEST
        if direction == "SouthEast":
            cmd = prepare_command(-speed, speed, 0)  # SOUTHEST
        if direction == "Stop":
            cmd = prepare_command(0, 0, 0)  # STOP
        if direction == "RTL":
            end = True
