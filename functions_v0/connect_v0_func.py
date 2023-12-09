from dronekit import connect


def connect_v0(self, origin, op_mode, external_client, internal_client, sending_topic):
    print(self.state)
    if self.state == 'disconnected':
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

        self.vehicle = connect(connection_string, wait_ready=False, baud=57600)

        self.vehicle.wait_ready(True, timeout=5000)

        print('Connected to flight controller')
        self.sending_telemetry_info = True
        self.state = 'connected'

        # return 'connected', vehicle

        # external_client.publish(sending_topic + "/connected", json.dumps(get_telemetry_info()))

    else:
        print('Autopilot already connected')


def disconnect(self):
    self.vehicle.close()
    self.sending_telemetry_info = False
    self.state = 'disconnected'
