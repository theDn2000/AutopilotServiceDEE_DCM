import threading
from dronekit import connect, Command, VehicleMode

import AutopilotServiceDEE_DCM.AutopilotService
from AutopilotServiceDEE_DCM.AutopilotService import state, sending_telemetry_info, vehicle  # noqa: F401
from AutopilotServiceDEE_DCM.functions_v0.send_telemetry_info_v0_func import send_telemetry_info_v0



def connect_v0(origin, op_mode, external_client, internal_client, sending_topic):
    global state
    global vehicle
    global sending_telemetry_info
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
        # vehicle = connect(connection_string, wait_ready=False, baud=57600)
        AutopilotServiceDEE_DCM.AutopilotService.vehicle = connect(connection_string, wait_ready=False, baud=57600)

        AutopilotServiceDEE_DCM.AutopilotService.vehicle.wait_ready(True, timeout=5000)
        #vehicle.wait_ready(True, timeout=5000)

        print('Connected to flight controller')
        state = 'connected'
        AutopilotServiceDEE_DCM.AutopilotService.sending_telemetry_info = True
        AutopilotServiceDEE_DCM.AutopilotService.state = 'connected'

        return 'connected', vehicle

        # external_client.publish(sending_topic + "/connected", json.dumps(get_telemetry_info()))

    else:
        print('Autopilot already connected')
