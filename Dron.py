class Dron(object):
    def __init__(self, broker):
        self.client = broker # necesita el broker para publicar respuestas
        self.state = "desconectado"
        ''' os otros estados son:
            conectado
            armando
            volando
            regresando
        '''

        self.going = False # se usa en dron_nav

    # aqui se importan los métodos de la clase Dron, que están organizados en ficheros.
    # Así podría orgenizarse la aportación de futuros alumnos que necesitasen incorporar nuevos servicios
    # para sus aplicaciones. Crearían un fichero con sus nuevos métodos y lo importarían aquí
    # Lo que no me gusta mucho es que si esa contribución nueva requiere de algún nuevo atributo de clase
    # ese atributo hay que declararlo aqui y no en el fichero con los métodos nuevos.
    # Ese es el caso del atributo going, que lo tengo que declarar aqui y preferiría poder declararlo en el fichero dron_goto

    from functions_v0.connect_v0_func import connect_v0
    from functions_v0.send_telemetry_info_v0_func import send_telemetry_info_trigger
    from functions_v0.get_telemetry_info_v0_func import get_telemetry_info
    from functions_v0.arm_v0_func import arm_v0
    from functions_v0.take_off_v0_func import take_off_trigger
    from functions_v0.return_to_launch_v0_func import returning_trigger
    from functions_v0.flying_v0_func import flying_trigger
    from functions_v0.goto_v0_func import goto_trigger