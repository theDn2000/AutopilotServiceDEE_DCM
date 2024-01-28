import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl
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
    print('recibo ', command)

    if command == "position":
        print("Position: ", message.payload)

    if command == "connect":

        dron.connect_v0(origin, op_mode, external_client, internal_client, sending_topic)

        # If connect is OK, initialize the telemetry data
        if dron.state == 'connected':
            dron.send_telemetry_info_trigger(external_client, internal_client, sending_topic)

    if command == "disconnect":
        if dron.state == 'connected':
            dron.disconnect()
        else:
            print('Vehicle is not connected')

    if command == "takeOff":

        if dron.state == 'armed' or 'onHearth':
            dron.take_off_trigger()
            # The script waits for the take_off to finish

        if dron.state == 'flying':
            dron.flying_trigger()

    if command == "returnToLaunch":
        # stop the process of getting positions
        dron.returning_trigger()

    if command == "armDrone":

        if dron.state == 'connected' or 'onHearth' or 'disarmed':
            dron.arm_v0()
            print(dron.state)
        else:
            print('The vehicle is not armable as it is not connected')

        # the vehicle will disarm automatically is takeOff does not come soon
        # when attribute 'armed' changes run function armed_change

        # dron.vehicle.add_attribute_listener('armed', dron.armed_change())

    if command == "disarmDrone":
        if dron.state == 'armed':
            dron.disarm()

    if command == "goto":
        if dron.state == 'flying':
            dron.goto_trigger(internal_client, external_client, sending_topic)
        else:
            print('Vehicle not flying')

    if command == "land":
        if dron.state == 'flying':

            # ENABLE GEOFENCE:
            param_name = "FENCE_ENABLE"
            param_value = 1
            if dron.get_parameter(param_name) != param_value:
                dron.modify_parameter(param_name, param_value)
                print("GEOFENCE ENABLED")
            else:
                print("GEOFENCE is already enabled")

            # CLEAR MISSION
            dron.clear_Mission()
            # CLEAR FENCE
            dron.clear_GEOFence()

            # DEFINE SPACE (Boundaries of )
            fencelist = [(-35.363925, 149.164797,), # 0th index: return point of this fence
                         (-35.363925, 149.164797,), # 1st index: same as the Nth index
                         (-35.362147, 149.164465,),
                         (-35.361924, 149.166149,),
                         (-35.363715, 149.166455,),
                         (-35.363925, 149.164797,)] # Nth index: same as the 1st index

            # ENABLE WAYPOINT LIMIT:
            param_name = "FENCE_TOTAL"
            param_value = len(fencelist)
            dron.modify_parameter(param_name, param_value)
            print("Fence total: ", dron.get_parameter(param_name))

            # SET GEOFENCE:
            dron.set_geofence(fence_list=fencelist)  # Upload GEOFence
            # dron.prepare_geofence(fencelist)  # Upload GEOFence
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
    dron = Dron(internal_client, external_client)

    AutopilotService(connection_mode, operation_mode, external_broker, username, password, internal_client,
                     external_client)
