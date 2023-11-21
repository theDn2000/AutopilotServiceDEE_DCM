import threading
from dronekit import connect, Command, VehicleMode
import time
from pymavlink import mavutil

import AutopilotServiceDEE_DCM.AutopilotService
from AutopilotServiceDEE_DCM.functions_v0.send_telemetry_info_v0_func import send_telemetry_info_v0
from AutopilotServiceDEE_DCM.functions_v0 import variables

def flying_v0():
    global direction
    global go
    speed = 1
    end = False
    cmd = prepare_command(0, 0, 0)  # stop
    while not end:
        AutopilotServiceDEE_DCM.functions_v0.variables.go = False
        while not AutopilotServiceDEE_DCM.functions_v0.variables.go:
            AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.send_mavlink(cmd)
            time.sleep(1)
        # a new go command has been received. Check direction
        print ('salgo del bucle por ', AutopilotServiceDEE_DCM.functions_v0.variables.direction)
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "North":
            cmd = prepare_command(speed, 0, 0)  # NORTH
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "South":
            cmd = prepare_command(-speed, 0, 0)  # SOUTH
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "East":
            cmd = prepare_command(0, speed, 0)  # EAST
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "West":
            cmd = prepare_command(0, -speed, 0)  # WEST
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "NorthWest":
            cmd = prepare_command(speed, -speed, 0)  # NORTHWEST
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "NorthEast":
            cmd = prepare_command(speed, speed, 0)  # NORTHEST
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "SouthWest":
            cmd = prepare_command(-speed, -speed, 0)  # SOUTHWEST
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "SouthEast":
            cmd = prepare_command(-speed, speed, 0)  # SOUTHEST
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "Stop":
            cmd = prepare_command(0, 0, 0)  # STOP
        if AutopilotServiceDEE_DCM.functions_v0.variables.direction == "RTL":
            end = True


def prepare_command(velocity_x, velocity_y, velocity_z):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.message_factory.set_position_target_local_ned_encode(
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