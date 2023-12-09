import json
import math

import threading
import paho.mqtt.client as mqtt
import time
import dronekit
from dronekit import connect, Command, VehicleMode
from paho.mqtt.client import ssl
from pymavlink import mavutil

from Dron import Dron

import AutopilotServiceDEE_DCM.functions_v0.variables
# Import functions from the function folder
from functions_v0 import connect_v0_func, get_telemetry_info_v0_func, send_telemetry_info_v0_func, arm_v0_func
from functions_v0.send_telemetry_info_v0_func import send_telemetry_info_v0
from functions_v0.take_off_v0_func import take_off_v0, take_off_trigger
from functions_v0.flying_v0_func import flying_v0, go_order, flying_trigger
from functions_v0.return_to_launch_v0_func import returning_v0, returning_trigger
from functions_v0.goto_v0_func import goto_v0, goto_trigger
from functions_v0 import variables

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

        Dron.connect_v0(origin, op_mode, external_client, internal_client, sending_topic)
        #connect_v0_func.connect_v0(origin, op_mode, external_client, internal_client, sending_topic)

        # If connect is OK, initialize the telemetry data
        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'connected':
            send_telemetry_info_v0_func.send_telemetry_info_trigger(external_client, internal_client, sending_topic)

    if command == "disconnect":
        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'connected':
            connect_v0_func.disconnect()
        else:
            print('Vehicle is not connected')

    if command == "takeOff":

        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'armed' or 'onHearth':
            take_off_trigger()
            # The script waits for the take_off to finish

        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'flying':
            flying_trigger()

    if command == "returnToLaunch":
        # stop the process of getting positions
        returning_trigger()

    if command == "armDrone":

        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'connected' or 'onHearth' or 'disarmed':
            arm_v0_func.arm_v0()
            print(AutopilotServiceDEE_DCM.functions_v0.variables.state)
        else:
            print('The vehicle is not armable as it is not connected')

        # the vehicle will disarm automatically is takeOff does not come soon
        # when attribute 'armed' changes run function armed_change

        AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.add_attribute_listener('armed', arm_v0_func.armed_change())

    if command == "disarmDrone":
        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'armed':
            arm_v0_func.disarm()

    if command == "land":
        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'flying':
            goto_trigger(internal_client, external_client, sending_topic)
        else:
            print('Vehicle not flying')

    if command == "go":
        if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'flying':
            go_order(message.payload.decode("utf-8"))
        else:
            print('Vehicle is not flying')


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
