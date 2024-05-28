import threading
import pymavlink
from pymavlink.mavutil import default_native
import pymavlink.dialects.v20.all as dialect


class Dron(object):
    def __init__(self, ID):
        self.ID = ID # ID del dron
        self.vehicle = None # objeto MAVLink (se inicia en el método connect)
        self.lock = threading.Lock()  # para evitar que se solapen las publicaciones de los dos hilos
        self.state = "disconnected"
        ''' os otros estados son:
            connected
            armed
            flying
            returning
        '''
        self.lat = 0
        self.lon = 0
        self.alt = 0

        self.sending_telemetry_info = False
        self.going = False  # se usa en dron_nav
        self.reaching_waypoint = False
        self.direction = "init"

    # aqui se importan los métodos de la clase Dron, que están organizados en ficheros.
    # Así podría orgenizarse la aportación de futuros alumnos que necesitasen incorporar nuevos servicios
    # para sus aplicaciones. Crearían un fichero con sus nuevos métodos y lo importarían aquí
    # Lo que no me gusta mucho es que si esa contribución nueva requiere de algún nuevo atributo de clase
    # ese atributo hay que declararlo aqui y no en el fichero con los métodos nuevos.
    # Ese es el caso del atributo going, que lo tengo que declarar aqui y preferiría poder declararlo en el fichero dron_goto

    from functions.connect_func import connect, disconnect
    from functions.telemetry_info_func import send_telemetry_info_trigger, get_telemetry_info, send_telemetry_info_MAVLINK
    from functions.arm_func import arm, arm_trigger, check_armed, check_armed_on_loop
    from functions.take_off_func import take_off, takeOff_MAVLINK
    from functions.altitude_func import change_altitude, change_altitude_trigger
    from functions.land_func import land, land_trigger
    from functions.return_to_launch_func import return_to_launch, returnToLaunch_MAVLINK
    from functions.flying_func import flying_trigger, flying_v0, prepare_command, go_order, check_flying_trigger, check_flying
    from functions.goto_func import goto, distanceInMeters, goto_MAVLINK, distanceInMeters
    from functions.geofence import clear_GEOFence, clear_Mission, geofence_trigger, enable_geofence, disable_geofence, set_fence_geofence, action_geofence
    from functions.modify_parameters import modify_parameter, get_parameter, get_all_parameters, get_position
    from functions.mission import uploadFlightPlan, executeFlightPlan, uploadFlightPlan_trigger, executeFlightPlan_trigger