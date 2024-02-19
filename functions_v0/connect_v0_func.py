from dronekit import connect
import json
import threading
import time
from pymavlink import mavutil
import sys
import itertools



def connect_v0(self, origin, op_mode, external_client, internal_client, sending_topic):
    # print("The current state is: " + self.state + " , trying to connect...")
    if self.state == 'disconnected':
        print("- Autopilot Service: Connection request by " + origin)
        # para conectar este autopilotService al dron al mismo tiempo que conectamos el Mission Planner
        # hay que ejecutar el siguiente comando desde PowerShell desde  C:\Users\USER>
        # mavproxy - -master =COM12 - -out = udp:127.0.0.1: 14550 - -out = udp:127.0.0.1: 14551
        # ahora el servicio puede conectarse por udp a cualquira de los dos puertos 14550 o 14551 y Mission Planner
        # al otro

        if op_mode == 'simulation':
            print('Simulation mode selected')
            connection_string = "tcp:127.0.0.1:5763"
            # connection_string = "udp:127.0.0.1:14550"
            # connection_string = "com7"
        else:
            print ('Real mode selected')
            # connection_string = "/dev/ttyS0"
            connection_string = "com7"
            # connection_string = "udp:127.0.0.1:14550"

        done = False
        #here is the animation
        def animate():
            for c in itertools.cycle(['|', '/', '-', '\\']):
                if done:
                    break
                sys.stdout.write('\rConnecting ' + c)
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write('\rConnected to flight controller     \n')

        t = threading.Thread(target=animate)
        t.start()

        self.vehicle = mavutil.mavlink_connection(connection_string)
        self.vehicle.wait_heartbeat()
        # self.vehicle = connect(connection_string, wait_ready=False, baud=57600)
        # self.vehicle.wait_ready(True, timeout=5000)

        time.sleep(1)
        done = True
        time.sleep(1)
        # time.sleep(5)
        # print('Connected to flight controller')

        self.sending_telemetry_info = True
        self.state = 'connected'

        # external_client.publish(sending_topic + "/connected", json.dumps(get_telemetry_info()))

    else:
        print('- Autopilot Service: '+origin+' already connected')

def disconnect(self):
    self.vehicle.close()
    self.sending_telemetry_info = False
    self.state = 'disconnected'
