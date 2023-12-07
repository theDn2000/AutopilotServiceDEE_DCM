from dronekit import connect

import AutopilotServiceDEE_DCM.AutopilotService


def connect_v0(origin, op_mode, external_client, internal_client, sending_topic):
    global state
    global vehicle
    global sending_telemetry_info
    if AutopilotServiceDEE_DCM.functions_v0.variables.state == 'disconnected':
        print("Autopilot service connected by " + origin)
        # para conectar este autopilotService al dron al mismo tiempo que conectamos el Mission Planner
        # hay que ejecutar el siguiente comando desde PowerShell desde  C:\Users\USER>
        # mavproxy - -master =COM12 - -out = udp:127.0.0.1: 14550 - -out = udp:127.0.0.1: 14551
        # ahora el servicio puede conectarse por udp a cualquira de los dos puertos 14550 o 14551 y Mission Planner
        # al otro

        if op_mode == 'simulation':
            connection_string = "tcp:127.0.0.1:5763"
            # connection_string = "tcp:192.168.208.2:5763"
            # connection_string = "udp:127.0.0.1:14550"
            # connection_string = "com7"
        else:
            # connection_string = "/dev/ttyS0"
            connection_string = "com7"
            # connection_string = "udp:127.0.0.1:14550"

        # vehicle = connect(connection_string, wait_ready=False, baud=115200)
        # vehicle = connect(connection_string, wait_ready=False, baud=57600)
        AutopilotServiceDEE_DCM.functions_v0.variables.vehicle = connect(connection_string, wait_ready=False, baud=57600)

        AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.wait_ready(True, timeout=5000)
        #vehicle.wait_ready(True, timeout=5000)

        print('Connected to flight controller')
        state = 'connected'
        AutopilotServiceDEE_DCM.functions_v0.variables.sending_telemetry_info = True
        AutopilotServiceDEE_DCM.functions_v0.variables.state = 'connected'

        # return 'connected', vehicle

        # external_client.publish(sending_topic + "/connected", json.dumps(get_telemetry_info()))

    else:
        print('Autopilot already connected')


def disconnect():
    AutopilotServiceDEE_DCM.functions_v0.variables.vehicle.close()
    AutopilotServiceDEE_DCM.functions_v0.variables.sending_telemetry_info = False
    AutopilotServiceDEE_DCM.functions_v0.variables.state = 'disconnected'