import threading
import pymavlink
from pymavlink.mavutil import default_native
import pymavlink.dialects.v20.all as dialect


class Dron(object):
    def __init__(self, internal_broker, external_broker):
        self.internal_client = internal_broker  # necesita el broker interno para publicar respuestas
        self.external_client = external_broker  # necesita el broker externo para publicar respuestas
        self.lock = threading.Lock()  # para evitar que se solapen las publicaciones de los dos hilos
        self.state = "disconnected"
        ''' os otros estados son:
            connected
            armed
            flying
            returning
        '''

        self.going = False  # se usa en dron_nav
        self.reaching_waypoint = False
        self.direction = "init"

    # aqui se importan los métodos de la clase Dron, que están organizados en ficheros.
    # Así podría orgenizarse la aportación de futuros alumnos que necesitasen incorporar nuevos servicios
    # para sus aplicaciones. Crearían un fichero con sus nuevos métodos y lo importarían aquí
    # Lo que no me gusta mucho es que si esa contribución nueva requiere de algún nuevo atributo de clase
    # ese atributo hay que declararlo aqui y no en el fichero con los métodos nuevos.
    # Ese es el caso del atributo going, que lo tengo que declarar aqui y preferiría poder declararlo en el fichero dron_goto

    from functions_v0.connect_v0_func import connect_v0, disconnect
    from functions_v0.telemetry_info_v0_func import send_telemetry_info_trigger, send_telemetry_info_v0, \
        get_telemetry_info, send_telemetry_info_MAMVLINK
    from functions_v0.arm_v0_func import arm_v0, armed_change, disarm, arm_MAVLINK
    from functions_v0.take_off_v0_func import take_off_trigger, take_off_v0, takeOff_MAVLINK
    from functions_v0.return_to_launch_v0_func import returning_trigger, returning_v0, returnToLaunch_MAVLINK
    from functions_v0.flying_v0_func import flying_trigger, flying_v0, prepare_command, go_order
    from functions_v0.goto_v0_func import goto_trigger, goto_v0, distanceInMeters
    from functions_v0.geofence import clear_GEOFence, upload_GEOFence, command_long_send, clear_Mission, prepare_geofence, set_geofence
    from functions_v0.modify_parameters import modify_parameter, get_parameter
