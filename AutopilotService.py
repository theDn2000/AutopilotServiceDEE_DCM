import json
import math

import threading
import paho.mqtt.client as mqtt
import time
import dronekit
from dronekit import connect, Command, VehicleMode
from paho.mqtt.client import ssl
from pymavlink import mavutil

import AutopilotServiceDEE_DCM.functions_v0.variables
# Import functions from the function folder
from functions_v0 import connect_v0_func, get_telemetry_info_v0_func, send_telemetry_info_v0_func, arm_v0_func
from functions_v0.send_telemetry_info_v0_func import send_telemetry_info_v0
from functions_v0.take_off_v0_func import take_off_v0
from functions_v0.flying_v0_func import flying_v0
from functions_v0 import variables

# Import and init global :
sending_telemetry_info = False
vehicle = object
state = 'disconnected'


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


def returning():
    global sending_telemetry_info
    global external_client
    global internal_client
    global sending_topic
    global state

    # wait until the drone is at home
    while AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.armed:
        time.sleep(1)
    AutopilotServiceDEE_DCM.functions_v0.variables.state = 'onHearth'




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


def executeFlightPlan(waypoints_json):
    global vehicle
    global internal_client, external_client
    global sending_topic
    global state

    altitude = 6
    origin = sending_topic.split('/')[1]

    waypoints = json.loads(waypoints_json)

    state = 'arming'
    # arm()
    state = 'takingOff'
    # take_off(altitude, False)
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
    # arm()
    state = 'takingOff'
    # take_off(altitude, False)
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
        connect_v0_func.connect_v0(origin, op_mode, external_client, internal_client, sending_topic)

        # If connect is OK, initialize the telemetry data
        print(AutopilotServiceDEE_DCM.functions_v0.variables.state)
        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'connected':
            AutopilotServiceDEE_DCM.functions_v0.variables.sending_telemetry_info = True
            y = threading.Thread(target=send_telemetry_info_v0, args=[external_client, internal_client, sending_topic])
            y.start()

    if command == "disconnect":
        AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.close()
        AutopilotServiceDEE_DCM.functions_v0.variables.sending_telemetry_info = False
        AutopilotServiceDEE_DCM.functions_v0.variables.state = 'disconnected'

    if command == "takeOff":

        print(AutopilotServiceDEE_DCM.functions_v0.variables.state)
        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'armed':
            # state = 'takingOff'
            w = threading.Thread(target=take_off_v0, args=[5, True])
            w.start()
            w.join()

        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'flying':
            w = threading.Thread(target=flying_v0)
            w.start()

    if command == "returnToLaunch":
        # stop the process of getting positions
        AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.mode = dronekit.VehicleMode("RTL")
        AutopilotServiceDEE_DCM.functions_v0.variables.state = 'returningHome'
        AutopilotServiceDEE_DCM.functions_v0.variables.direction = "RTL"
        AutopilotServiceDEE_DCM.functions_v0.variables.go = True
        w = threading.Thread(target=returning)
        w.start()

    if command == "armDrone":

        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'connected':
            arm_v0_func.arm_v0()
            print(AutopilotServiceDEE_DCM.functions_v0.variables.state)
        # arm()
        else:
            print('The vehicle is not armable as it is not connected')

        # the vehicle will disarm automatically is takeOff does not come soon
        # when attribute 'armed' changes run function armed_change

        # DESCOMENTAR ESTO
        # vehicle.add_attribute_listener('armed', armed_change)
        # state = 'armed'

    if command == "disarmDrone":
        AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.armed = False
        while AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.armed:
            time.sleep(1)
        AutopilotServiceDEE_DCM.functions_v0.variables.state = 'disarmed'

    if command == "land":

        vehicle.mode = dronekit.VehicleMode("LAND")
        state = 'landing'
        while vehicle.armed:
            time.sleep(1)
        state = 'onHearth'

    if command == "go":
        AutopilotServiceDEE_DCM.functions_v0.variables.direction = message.payload.decode("utf-8")
        print("Going ", AutopilotServiceDEE_DCM.functions_v0.variables.direction)
        AutopilotServiceDEE_DCM.functions_v0.variables.go = True

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


def on_connect(external_client, userdata, flags, rc):
    if rc == 0:
        print("Connection OK")
    else:
        print("Bad connection")


def AutopilotService(connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client
    global state

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
    variables.init()
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
