import threading
from dronekit import connect, Command, VehicleMode
from AutopilotServiceDEE_DCM.functions.processes import send_telemetry_info
from AutopilotService import state, vehicle


def on_connect(origin, op_mode):
    global state
    global vehicle
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
