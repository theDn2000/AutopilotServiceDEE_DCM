import json
import math

import threading
import paho.mqtt.client as mqtt
import time
import dronekit
from dronekit import connect, Command, VehicleMode
from paho.mqtt.client import ssl
from pymavlink import mavutil

# Import initialization functions:
from functions.init import on_connect, arm

# Import processes functions:
from functions.processes import prepare_command, get_telemetry_info

# Import mobility functions:
from functions.actions.mobility import set_direction

# Import calculations functions:
from functions.actions.calculations import distanceInMeters

# Take off como depende de flying no puedo moverlo:
def take_off(a_target_altitude, manualControl):
    global state
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
        w = threading.Thread(target=flying)
        w.start()

'''
These are the different values for the state of the autopilot:
    'connected' (only when connected the telemetry_info packet will be sent every 250 miliseconds)
    'arming'
    'armed'
    'disarmed'
    'takingOff'
    'flying'
    'returningHome'
    'landing'
    'onHearth'

The autopilot can also be 'disconnected' but this state will never appear in the telemetry_info packet 
when disconnected the service will not send any packet
'''

def send_telemetry_info():
    global external_client
    global sending_telemetry_info
    global sending_topic

    while sending_telemetry_info:
        external_client.publish(sending_topic + "/telemetryInfo", json.dumps(get_telemetry_info(vehicle, state)))
        time.sleep(0.25)


def returning():
    global sending_telemetry_info
    global external_client
    global internal_client
    global sending_topic
    global state

    # wait until the drone is at home
    while vehicle.armed:
        time.sleep(1)
    state = 'onHearth'

# Flying deja de funcionar si lo muevo y lo exporto, por temas de threading y de variables globales, el movimiento deja de funcionar
def flying():
    global go
    global vehicle
    global direction
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


def executeFlightPlan(waypoints_json):
    global vehicle
    global internal_client, external_client
    global sending_topic
    global state

    altitude = 6
    origin = sending_topic.split('/')[1]

    waypoints = json.loads(waypoints_json)

    state = 'arming'
    arm(vehicle)
    state = 'takingOff'
    take_off(altitude, False)
    state = 'flying'
    # vehicle.groundspeed=3

    wp = waypoints[0]
    originPoint = dronekit.LocationGlobalRelative(float(wp['lat']), float(wp['lon']), altitude)

    distanceThreshold = 0.50
    for wp in waypoints[1:]:

        destinationPoint = dronekit.LocationGlobalRelative(float(wp['lat']), float(wp['lon']), altitude)
        vehicle.simple_goto(destinationPoint, groundspeed=3)

        currentLocation = vehicle.location.global_frame
        dist = distanceInMeters(destinationPoint, currentLocation)

        while dist > distanceThreshold:
            time.sleep(0.25)
            currentLocation = vehicle.location.global_frame
            dist = distanceInMeters(destinationPoint, currentLocation)
        print('reached')
        waypointReached = {
            'lat': currentLocation.lat,
            'lon': currentLocation.lon
        }

        external_client.publish(sending_topic + "/waypointReached", json.dumps(waypointReached))

        if wp['takePic']:
            # ask to send a picture to origin
            internal_client.publish(origin + "/cameraService/takePicture")

    vehicle.mode = dronekit.VehicleMode("RTL")
    state = 'returningHome'

    currentLocation = vehicle.location.global_frame
    dist = distanceInMeters(originPoint, currentLocation)

    while dist > distanceThreshold:
        time.sleep(0.25)
        currentLocation = vehicle.location.global_frame
        dist = distanceInMeters(originPoint, currentLocation)

    state = 'landing'
    while vehicle.armed:
        time.sleep(1)
    state = 'onHearth'


def executeFlightPlan2(waypoints_json):
    global vehicle
    global internal_client, external_client
    global sending_topic
    global state

    altitude = 6
    origin = sending_topic.split('/')[1]

    waypoints = json.loads(waypoints_json)
    state = 'arming'
    arm(vehicle)
    state = 'takingOff'
    take_off(altitude, False)
    state = 'flying'
    cmds = vehicle.commands
    cmds.clear()

    # wp = waypoints[0]
    # originPoint = dronekit.LocationGlobalRelative(float(wp['lat']), float(wp['lon']), altitude)
    for wp in waypoints:
        cmds.add(
            Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0,
                    0, 0, 0, 0, float(wp['lat']), float(wp['lon']), altitude))
    wp = waypoints[0]
    cmds.add(
        Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0,
                0, 0, 0, 0, float(wp['lat']), float(wp['lon']), altitude))
    cmds.upload()

    vehicle.commands.next = 0
    # Set mode to AUTO to start mission
    vehicle.mode = VehicleMode("AUTO")
    while True:
        nextwaypoint = vehicle.commands.next
        print('next ', nextwaypoint)
        if nextwaypoint == len(waypoints):  # Dummy waypoint - as soon as we reach waypoint 4 this is true and we exit.
            print("Last waypoint reached")
            break;
        time.sleep(0.5)

    print('Return to launch')
    state = 'returningHome'
    vehicle.mode = VehicleMode("RTL")
    while vehicle.armed:
        time.sleep(1)
    state = 'onHearth'


# Todas las funciones que se ejecutan directamente desde process_message se hacen con threads, lo que implica que tengo que pasar las variables a las funciones que inicio con threads. PASO INTERMEDIO?????????
def process_message(message, client):
    global vehicle
    global direction
    global go
    global sending_telemetry_info
    global sending_topic
    global op_mode
    global sending_topic
    global state

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    sending_topic = "autopilotService/" + origin
    print('recibo ', command)

    if command == "position":
        print("Position: ", message.payload)

    if command == "connect":
        if state == 'disconnected':
            print("Autopilot service connected by " + origin)
            # para conectar este autopilotService al dron al mismo tiempo que conectamos el Mission Planner
            # hay que ejecutar el siguiente comando desde PowerShell desde  C:\Users\USER>
            # mavproxy - -master =COM12 - -out = udp:127.0.0.1: 14550 - -out = udp:127.0.0.1: 14551
            # ahora el servicio puede conectarse por udp a cualquira de los dos puertos 14550 o 14551 y Mission Planner
            # al otro

            if op_mode == 'simulation':
                connection_string = "tcp:127.0.0.1:5763"
                # connection_string = "udp:127.0.0.1:14550"
                # connection_string = "com7"
            else:
                # connection_string = "/dev/ttyS0"
                connection_string = "com7"
                # connection_string = "udp:127.0.0.1:14550"

            # vehicle = connect(connection_string, wait_ready=False, baud=115200)
            vehicle = connect(connection_string, wait_ready=False, baud=57600)

            vehicle.wait_ready(True, timeout=5000)

            print('Connected to flight controller')
            state = 'connected'

            # external_client.publish(sending_topic + "/connected", json.dumps(get_telemetry_info()))

            sending_telemetry_info = True
            y = threading.Thread(target=send_telemetry_info)
            y.start()
        else:
            print('Autopilot already connected')

    if command == "disconnect":
        vehicle.close()
        sending_telemetry_info = False
        state = 'disconnected'

    if command == "takeOff":
        state = 'takingOff'
        w = threading.Thread(target=take_off, args=[5, True])
        w.start()

    if command == "returnToLaunch":
        # stop the process of getting positions
        vehicle.mode = dronekit.VehicleMode("RTL")
        state = 'returningHome'
        direction = "RTL"
        go = True
        w = threading.Thread(target=returning)
        w.start()

    if command == "armDrone":
        print('arming')
        state = 'arming'
        arm(vehicle)

        # the vehicle will disarm automatically is takeOff does not come soon
        # when attribute 'armed' changes run function armed_change
        vehicle.add_attribute_listener('armed', armed_change)
        state = 'armed'

    if command == "disarmDrone":
        vehicle.armed = False
        while vehicle.armed:
            time.sleep(1)
        state = 'disarmed'

    if command == "land":

        vehicle.mode = dronekit.VehicleMode("LAND")
        state = 'landing'
        while vehicle.armed:
            time.sleep(1)
        state = 'onHearth'

    if command == "go":
        direction = message.payload.decode("utf-8")
        print("Going ", direction)
        go = True

    if command == 'executeFlightPlan':
        waypoints_json = str(message.payload.decode("utf-8"))
        w = threading.Thread(target=executeFlightPlan, args=[waypoints_json, ])
        w.start()

    if command == 'videoFrameWithColor':
        # ya se está moviendo. Solo entonces hacemos caso de los colores
        frameWithColor = json.loads(message.payload)
        d = set_direction(frameWithColor['color'])
        if d != 'none':
            direction = d
            if direction == 'RTL':
                vehicle.mode = dronekit.VehicleMode("RTL")
                print('cambio estado')
                state = 'returningHome'
                w = threading.Thread(target=returning)
                w.start()

            go = True


def armed_change(self, attr_name, value):
    global vehicle
    global state
    print('cambio a ', )
    if vehicle.armed:
        state = 'armed'
    else:
        state = 'disarmed'

    print('cambio a ', state)


def on_internal_message(client, userdata, message):
    global internal_client
    process_message(message, internal_client)


def on_external_message(client, userdata, message):
    global external_client
    process_message(message, external_client)


def AutopilotService(connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client
    global state

    state = 'disconnected'

    print('Connection mode: ', connection_mode)
    print('Operation mode: ', operation_mode)
    op_mode = operation_mode

    internal_client = mqtt.Client("Autopilot_internal")
    internal_client.on_message = on_internal_message
    internal_client.connect("localhost", 1884)

    external_client = mqtt.Client("Autopilot_external", transport="websockets")
    external_client.on_message = on_external_message
    external_client.on_connect = on_connect

    if connection_mode == "global":
        if external_broker == "hivemq":
            external_client.connect("broker.hivemq.com", 8000)
            print('Connected to broker.hivemq.com:8000')

        elif external_broker == "hivemq_cert":
            external_client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                                    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            external_client.connect("broker.hivemq.com", 8884)
            print('Connected to broker.hivemq.com:8884')

        elif external_broker == "classpip_cred":
            external_client.username_pw_set(
                username, password
            )
            external_client.connect("classpip.upc.edu", 8000)
            print('Connected to classpip.upc.edu:8000')

        elif external_broker == "classpip_cert":
            external_client.username_pw_set(
                username, password
            )
            external_client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                                    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            external_client.connect("classpip.upc.edu", 8883)
            print('Connected to classpip.upc.edu:8883')
        elif external_broker == "localhost":
            external_client.connect("localhost", 8000)
            print('Connected to localhost:8000')
        elif external_broker == "localhost_cert":
            print('Not implemented yet')

    elif connection_mode == "local":
        if operation_mode == "simulation":
            external_client.connect("localhost", 8000)
            print('Connected to localhost:8000')
        else:
            external_client.connect("10.10.10.1", 8000)
            print('Connected to 10.10.10.1:8000')

    print("Waiting....")
    external_client.subscribe("+/autopilotService/#", 2)
    external_client.subscribe("cameraService/+/#", 2)
    internal_client.subscribe("+/autopilotService/#")
    internal_client.loop_start()
    if operation_mode == 'simulation':
        external_client.loop_forever()
    else:
        # external_client.loop_start() #when executed on board use loop_start instead of loop_forever
        external_client.loop_forever()


if __name__ == '__main__':

    # Define all the global variables:
    global state
    global external_client
    global sending_telemetry_info
    global sending_topic
    global internal_client
    global direction
    global go
    global vehicle
    global op_mode
    import sys

    connection_mode = sys.argv[1]  # global or local
    operation_mode = sys.argv[2]  # simulation or production
    username = None
    password = None
    if connection_mode == 'global':
        external_broker = sys.argv[3]
        if external_broker == 'classpip_cred' or external_broker == 'classpip_cert':
            username = sys.argv[4]
            password = sys.argv[5]
    else:
        external_broker = None

    AutopilotService(connection_mode, operation_mode, external_broker, username, password)
