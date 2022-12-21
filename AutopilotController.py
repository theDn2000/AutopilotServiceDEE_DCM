import threading

import paho.mqtt.client as mqtt
import time

import dronekit
from dronekit import connect
from pymavlink import mavutil


local_broker_address = "localhost"
local_broker_port = 1883
led_sequence_on = False


def arm():
    """Arms vehicle and fly to aTargetAltitude."""
    print("Basic pre-arm checks")  # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = dronekit.VehicleMode("GUIDED")
    vehicle.armed = True
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)


def take_off(a_target_altitude):
    vehicle.simple_takeoff(a_target_altitude)
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= a_target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


def prepare_command(velocity_x, velocity_y, velocity_z):
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


def send_position():
    global client
    global sending_positions

    while sending_positions:
        lat = vehicle.location.global_frame.lat
        lon = vehicle.location.global_frame.lon
        position = str(lat) + "*" + str(lon)
        print("Send new position")
        client.publish("autopilotService/dataService/storePosition", position)
        time.sleep(0.25)


def returning():
    global sending_positions
    # wait until the drone is at home
    while vehicle.armed:
        time.sleep(1)
    print("At home")
    vehicle.close()
    sending_positions = False


def flying():
    global direction
    global go
    speed = 1
    end = False
    cmd = prepare_command(0, 0, 0)  # stop
    while not end:
        go = False
        while not go:
            vehicle.send_mavlink(cmd)
            time.sleep(1)
        # a new go command has been received. Check direction
        if direction == "North":
            cmd = prepare_command(speed, 0, 0)  # NORTH
        if direction == "South":
            cmd = prepare_command(-speed, 0, 0)  # SOUTH
        if direction == "East":
            cmd = prepare_command(0, speed, 0)  # EAST
        if direction == "West":
            cmd = prepare_command(0, -speed, 0)  # WEST
        if direction == "Stop":
            cmd = prepare_command(0, 0, 0)  # STOP
        if direction == "RTL":
            end = True

def on_message(client, userdata, message):
    global led_sequence_on
    global vehicle
    global direction
    global go
    global sending_positions

    positions = ["getDronePosition", "getHomePosition", "getDestinationPosition"]

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    sending_topic = "autopilotService/" + origin

    if command == "connectPlatform":
        print("Autopilot service connected by " + origin)
        client.subscribe("+/autopilotService/#")
        connection_string = "tcp:127.0.0.1:5763"
        vehicle = connect(connection_string, wait_ready=True, baud=115200)
        sending_positions = False
        y = threading.Thread(target=send_position)
        y.start()

    if command == "connect":
        client.publish("autopilotService/droneCircus/connected")

    if command == "armDrone":
        arm()
        if origin == "droneCircus":
            client.publish("autopilotService/droneCircus/armed")

    if command == "takeOff":
        if origin != "droneCircus":
            altitude = float(message.payload)
            take_off(altitude)
        else:
            take_off(5)
            client.publish("autopilotService/droneCircus/takenOff")
            w = threading.Thread(target=flying)
            w.start()

    if command == "getDroneHeading":
        client.publish(sending_topic + "/droneHeading", vehicle.heading)

    if command == "getDroneAltitude":
        client.publish(
            sending_topic + "/droneAltitude",
            vehicle.location.global_relative_frame.alt,
        )

    if command == "getDroneGroundSpeed":
        client.publish(
            sending_topic + "/droneGroundSpeed", vehicle.groundspeed
        )

    if command in positions:
        lat = vehicle.location.global_frame.lat
        lon = vehicle.location.global_frame.lon
        position = str(lat) + "*" + str(lon)
        if command == positions[0]:
            client.publish(sending_topic + "/dronePosition", position)
        if command == positions[1]:
            client.publish(sending_topic + "/homePosition", position)
        if command == positions[2]:
            client.publish(sending_topic + "/destinationPosition", position)

    if command == "goToPosition":
        position_str = str(message.payload.decode("utf-8"))
        position = position_str.split("*")
        lat = float(position[0])
        lon = float(position[1])
        point = dronekit.LocationGlobalRelative(lat, lon, 20)
        vehicle.simple_goto(point)
        # we start a procedure to get the drone position every 5 seconds
        # and send it to the data service (to be stored there)
        go = True

    if command == "returnToLaunch":
        # stop the process of getting positions
        vehicle.mode = dronekit.VehicleMode("RTL")
        direction = "RTL"
        go = True
        w = threading.Thread(target=returning)
        w.start()

    if command == "disarmDrone":
        vehicle.armed = True

    if command == "go":
        direction = message.payload.decode("utf-8")
        print("Going ", direction)
        go = True


client = mqtt.Client("Autopilot service")
client.on_message = on_message
client.connect(local_broker_address, local_broker_port)
client.loop_start()
print("Waiting DASH connection ....")
client.subscribe("gate/autopilotService/connectPlatform")
