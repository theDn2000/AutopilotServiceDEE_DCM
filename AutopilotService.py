import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl
import json
import os
import sys

sys.path.append(os.path.abspath('../../..'))

from Dron import Dron

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
    print('- Autopilot Service: Received "' + command +'".')

    if command == "position":
        print("Position: ", message.payload)

    if command == "connect":

        dron.connect(origin, op_mode, external_client, internal_client, sending_topic, True)

        # If connect is OK, initialize the telemetry data
        if dron.state == 'connected':
            dron.send_telemetry_info_trigger(external_client, internal_client, sending_topic, process_output)

    if command == "disconnect":
        if dron.state == 'connected':
            dron.disconnect()
        else:
            print('Vehicle is not connected')

    if command == "takeOff":

        if dron.state == 'armed' or 'onHearth':
            print("- Autopilot Service: Vehicle taking off")
            dron.take_off(10, True)
            print("- Autopilot Service: Vehicle reached target altitude")
            # The script waits for the take_off to finish

        if dron.state == 'flying':
            dron.flying_trigger()

    if command == "returnToLaunch":
        # stop the process of getting positions
        dron.return_to_launch(False)

    if command == "armDrone":

        if dron.state == 'connected' or 'onHearth' or 'disarmed':
            dron.arm(True)
            print("- Autopilot Service: Vehicle armed")
        else:
            print('- Autopilot Service: The vehicle is not armable as it is not connected')

        # the vehicle will disarm automatically is takeOff does not come soon
        # when attribute 'armed' changes run function armed_change

        # dron.vehicle.add_attribute_listener('armed', dron.armed_change())

    if command == "disarmDrone":
        if dron.state == 'armed':
            dron.disarm()

    if command == "goto":
        if dron.state == 'flying':
            dron.goto(internal_client, external_client, sending_topic, lat=1, lon=1, blocking=True) # TEST
        else:
            print('Vehicle not flying')

    if command == "land":
        if dron.state == 'flying':
            # TEST MODIFY PARAMETERS
            print(dron.get_parameter_MAVLINK('RTL_ALT'))

            # TEST GEOFENCE
            #dron.geofence_trigger("enable")

        else:
            print('Vehicle not flying')

    if command == "go":
        if dron.state == 'flying':
            dron.go_order(message.payload.decode("utf-8"))
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


def process_output(telemetry_info):
    # Callback function to send the telemetry_info packet
    external_client.publish(sending_topic + '/telemetryInfo', json.dumps(telemetry_info))


def AutopilotService(connection_mode, operation_mode, external_broker, username, password, internal_client,
                     external_client):
    global op_mode
    global state

    print('Connection mode: ', connection_mode)
    print('Operation mode: ', operation_mode)
    op_mode = operation_mode

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

    # Broker interno:
    internal_client = mqtt.Client("Autopilot_internal")
    internal_client.on_message = on_internal_message
    # internal_client.connect("192.168.208.2", 1884)
    internal_client.connect("localhost", 1884)

    # Broker externo:
    external_client = mqtt.Client("Autopilot_external", transport="websockets")
    external_client.on_message = on_external_message
    external_client.on_connect = on_connect

    # Una vez definidos el broker interno y el externo, inicializamos el objeto Dron:
    ID = 1
    dron = Dron(ID)

    AutopilotService(connection_mode, operation_mode, external_broker, username, password, internal_client,
                     external_client)
