# DroneLink EETAC 

![logo](https://github.com/theDn2000/AutopilotServiceDEE_DCM/assets/109517814/18cc8967-327c-48f8-9cfc-2be24e8043ab)

## Content table
- [Introduction](https://github.com/theDn2000/AutopilotServiceDEE_DCM/edit/dev_v4.0-DroneLink/README.md#introduction)
- [Instalación](https://github.com/theDn2000/AutopilotServiceDEE_DCM/edit/dev_v4.0-DroneLink/README.md#-installation-and-requirements)
- [Contributions](https://github.com/theDn2000/AutopilotServiceDEE_DCM/edit/dev_v4.0-DroneLink/README.md#-contributions)
- [Use](https://github.com/theDn2000/AutopilotServiceDEE_DCM/edit/dev_v4.0-DroneLink/README.md#-use)

## Introduction

DroneLink EETAC es un proyecto diseñado para facilitar la interacción con drones a través del protocolo MAVLink, ofreciendo robustez y escalabilidad en el control del piloto automático y de sus cámaras. Este repositorio incluye la librería principal DroneLink EETAC, una librería adicional para el control de cámaras denominada CameraLink EETAC, y tres ejemplos prácticos que demuestran su versatilidad y potencial de aplicación. 

>[!NOTE]
>DroneLink EETAC es un módulo complementario de Drone Engineering Ecosystem, repositorio de la escuela de Ingeniería de Telecomunicación y Aeroespacial de Castelldefels.\
>\
> [![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-MainRepo-brightgreen.svg)](https://github.com/dronsEETAC/DroneEngineeringEcosystemDEE)

In this file usted encontrará tanto las instrucciones de instalación como una guía para el uso de las librerías, además de información sobre el funcionamiento de los ejemplos y sus características.

## 📦 Installation and Requirements

>[!CAUTION]
>Antes de instalar el proyecto, asegúrate de tener una versión de **Python 3.7 o superior**, es esencial para la ejecución de las librerías. Puedes descargarlo desde [python.org](https://www.python.org/downloads/)

Clona el repositorio en tu máquina local utilizando git:

```
git clone https://github.com/tu-usuario/tu-proyecto.git A MODIFICAR
cd DroneLink-EETAC
```

Una vez dispongas del repositorio, descarga las dependencias del archivo *requirements.txt*

```
pip install -r requirements.txt
```
Con esto estarás listo para usar tanto la librería DroneLink EETAC como CameraLink EETAC.

>[!WARNING]
>Si adicionalmente quieres usar los ejemplos incluidos en este repositorio, deberás disponer de última versión de las siguientes herramientas:
>- **Mission Planner**: Esencial para ejecutar las aplicaciones incluidas en modo simulación. Puedes descargarlo desde [MissionPlanner](https://ardupilot.org/planner/docs/mission-planner-installation.html).
>- **Eclipse Mosquitto**: Broker necesario para el ejemplo remoto en modo simulación. Puedes descargarlo desde [Mosquitto](https://mosquitto.org/download/)

## 🤝 Contributions

Este proyecto está destinado a crecer a partir de las contribucciones tanto de la escuela como externas. Si deseas conntribuir, sigue las siguientes indicaciones:

1. **Fork** el repositorio original:

   - Navega a la [página principal del proyecto en GitHub](https://github.com/tu-usuario/tu-proyecto). A MODIFICAR
   - Haz clic en el botón "Fork" en la esquina superior derecha de la página.
   - Esto creará una copia del repositorio en tu cuenta de GitHub.
  
2. **Clona** tu fork a tu máquina local:

   ```
   git clone https://github.com/tu-usuario-fork/tu-proyecto.git A MODIFICAR
   cd tu-proyecto
   ```

3. **Descarga** las dependencias del archivo *requirements.txt:
   ```
    pip install -r requirements.txt
    ```

4. Configura el repositorio original como un remoto adicional llamado **upstream**:

   ```
   git remote add upstream https://github.com/tu-usuario/tu-proyecto.git A MODIFICAR
   ```

5. Crea una nueva **rama** para trabajar en tus versión:

   ```
    git checkout -b nombre-de-tu-rama
   ```

Ahora puedes hacer pull requests desde tu fork y un administrador puede hacer merge de tus contribuciones al repositorio principal. 
   
>[!NOTE]
>This video show an example of how you can contribute to the project\
>\
>[![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-contributions-pink.svg)](https://www.youtube.com/watch?v=dv-k5MKjq8g) 
   
## 🚀 Use

### DroneLink EETAC

Para hacer uso de la librería DroneLink EETAC primero debes importar la clase Drone a tu proyecto. La clase Drone está definida en el fichero Drone.py.

```
from Drone import Drone
```

Una vez importada la librería, puedes crear un objeto tipo Drone para usarla. Para ello, deberás de pasarle el int ***id***, que se trata del identificador de ese dron en específico.

```
drone = Drone(id)
```

Con el objeto de tipo Dron creado, puedes llamar a las funciones del objeto Drone de la siguiente forma:

```
drone.function_name(parameter_1, parameter_2, etc)
```
A continuación se muestra una tabla con todas las funciones de las que dispone DroneLink EETAC:

Function | Description | Parameter 1 | Parameter 2 | Parameter 3 | Response
--- | --- | --- | --- | --- | ---
*connect* | Stablishes the MAVLink connection with the autopilot of the drone | connection string [str] | baud rate (115200 by default) [int] | No | No
*get_position* | Get the position of the drone | No | No | No | latitude, longitude, altitude
*disconnect* | Closes the MAVLink connection with the autopilot of the drone | No | No | No | No
*send_telemetry_info* | Sends the telemetry info of the drone | callback (callback function to interpret the information) | No | No | No
*arm* | Arms the drone | No | No | No | No
*check_armed* | Checks if the vehicle is armed or not | No | No | No | True or False
*take_off* | Get the drone take off to reach the desired altitude | target altitude (in meters) [int] | No | No | No
*change_altitude* | Get the drone reach the desired altitude during flight | target altitude (in meters) [int] | No | No | No
*go_order* | Makes the drone go in a specific direction | direction ("North", "South", "East", "West", "NorthWest", "NorthEast", "SouthWest", "SouthEast", "Stop" [str]) | No | No | No
*check_flying* | Checks if the drone is flying | No | No | No | True or False
*goto* | Make the drone go to a specific waypoint | latitude [float] | longitude [float] | altitude [int] | No
*land* | Land the drone | No | No | No | No
*return_to_launch* | Go to the launch position and land | No | No | No | No
*uploadFlightPlan* | Upload a flight plan to the vehicle | waypoints_json (JSON string with the coordinates of the waypoints, check the function for more information about the format) | No | No | No
*executeFlightPlan* | Execute the flight plan previously uploaded | No | No | No | No
*set_fence_geofence* | Upload a geofence to the vehicle | fence_list (tuple list with the geofence points, check the function for more information about the format) | No | No | No
*enable_geofence* | Enable the geofence | No | No | No | No
*disable_geofence* | Disable the geofence | No | No | No | No
*action_geofence* | Set the action of the drone when trespassing the geofence | action (0: Report, 1: RTL or Land, 2: Always Land, 3: Smart RTL or RTL or Land, 4: Brake or Land, 5: Smart RTL or Land) [int]| No | No | No
*get_parameter* | Get the value of a parameter of the autopilot | param_name (name of the parameter) [str] | No | No | value of the parameter
*get_all_parameters* | Get all the parameters of the autopilot | No | No | No | list of parameters names, list of parameters values
*modify_parameter* | Modify a parameter of the autopilot | param_name (name of the parameter) [str] | param_value (value of the parameter) [float] | No | No

>[!IMPORTANT]
>Además, las funciones que lo permiten, disponen de una versión alternativa donde podemos ejecutarlas escogiendo si queremos que sean bloqueantes o no bloqueantes:

Function | Description | Parameter 1 | Parameter 2 |  Parameter 3 | Parameter 4 | Response
--- | --- | --- | --- | --- | --- | ---
*connect_trigger* | Stablishes the MAVLink connection with the autopilot of the drone | connection string [str] | blocking (True or False) [bool] | baud rate (115200 by default) [int] | No | No
*send_telemetry_info_trigger* | Sends the telemetry info of the drone | callback (callback function to interpret the information) | blocking (True or False) [bool] | No | No | No
*arm_trigger* | Arms the drone | blocking (True or False) [bool] | No | No | No | No
*take_off_trigger* | Get the drone take off to reach the desired altitude | target altitude (in meters) [int] | blocking (True or False) [bool] | No | No | No
*change_altitude_trigger* | Get the drone reach the desired altitude during flight | target altitude (in meters) [int] | blocking (True or False) [bool] | No | No | No
*check_flying_trigger* | Checks if the drone is flying | blocking (True or False) [bool] | No | No | No | True or False
*goto_trigger* | Make the drone go to a specific waypoint | latitude [float] | longitude [float] | altitude [int] | blocking (True or False) [bool] | No
*land_trigger* | Land the drone | blocking (True or False) [bool] | No | No | No | No
*return_to_launch_trigger* | Go to the launch position and land | blocking (True or False) [bool] | No | No | No | No
*uploadFlightPlan_trigger* | Upload a flight plan to the vehicle | waypoints_json (JSON string with the coordinates of the waypoints, check the function for more information about the format) | blocking (True or False) [bool] | No | No | No
*executeFlightPlan_trigger* | Execute the flight plan previously uploaded | blocking (True or False) [bool] | No | No | No | No
*get_parameter_trigger* | Get the value of a parameter of the autopilot | param_name (name of the parameter) [str] | blocking (True or False) [bool] | No | No | value of the parameter
*get_all_parameters_trigger* | Get all the parameters of the autopilot | blocking (True or False) [bool] | No | No | No | list of parameters names, list of parameters values
*modify_parameter_trigger* | Modify a parameter of the autopilot | param_name (name of the parameter) [str] | param_value (value of the parameter) [float] | blocking (True or False) [bool] | No | No


The drone object has a parameter called **state**, which is modified depending on which functions are executed. The possible values of drone.state are the following:

- connected
- armed
- takingOff
- changingAltitude
- flying
- returningHome
- landing
- onMission

### CameraLink EETAC

Para hacer uso de la librería CameraLink EETAC primero debes importar la clase Camera a tu proyecto. La clase Camera está definida en el fichero Camera.py.

```
from Camera import Camera
```

Una vez importada la librería, puedes crear un objeto tipo Camera para usarla. Para ello, deberás de pasarle el int ***id***, que se trata del identificador de esa cámara en específico.

```
camera = Camera(id)
```

Con el objeto de tipo Camera creado, puedes llamar a las funciones del objeto Camera de la siguiente forma:

```
camera.function_name(parameter_1, parameter_2, etc)
```
A continuación se muestra una tabla con todas las funciones de las que dispone DroneLink EETAC:

Function | Description | Parameter 1 | Parameter 2 | Parameter 3 | Response
--- | --- | --- | --- | --- | ---
*take_picture* | Take a picture using the camera | No | No | No | jpg_as_text (image encoded in base64)
*start_video_stream* | Start video stream using the camera | callback (callback function to interpret every frame) | No | No | No
*stop_video_stream* | Stop video stream  | No | No | No | No










In order to send a command to the autopilot service, a module must publish a message in the external (or internal) broker. The topic of the message must be in the form:
```
"XXX/autopilotService/YYY"
```
where XXX is the name of the module requiring the service and YYY is the name of the service that is required. Oviously, some of the commands may require additional data that must be included in the payload of the message to be published. 
In some cases, after completing the service requiered the autopilot service publish a message as an answer. The topic of the answer has the format:
```
"autopilotService/XXX/ZZZ"
```
where XXX is the name of the module requiring the service and ZZZ is the answer. The message can include data in the message payload.

The table bellow indicates all the commands that are accepted by the autopilot service in the current version.   

Command | Description | Payload | Answer | Answer payload
--- | --- | --- | --- |--- 
*connect* | connect with the simulator or the flight controller depending on the operation mode | No | No (see Note 1) | No
*armDrone* | arms the drone (either simulated or real) | No | NO (see Note 2) | No 
*takeOff* | get the drone take off to reach and altitude of 5 meters | No | No (see Note 3)  | No 
*returnToLaunch* | go to launch position |No  | No (see Note 4) | No    
*land* | the dron will land |No  | No (see Note 5) | No     
*disarmDrone* | disarm the drone |No  |  No (see Note 6) | No 
*go* | move in certain direction |"North", "South", "East", "West", "NorthWest", "NorthEast", "SouthWest", "SouthEast" , "Stop"  | No | No 
*disconnect* | disconnect from the simulator or the flight controller depending on the operation mode | No | NO (see Note 1) | No
*executeFlightPlan* | execute the flight plan received | See Note 7 | see Note 7 | see Note 7


Note 1    
When the autopilot is connected the service will start sending telemetry_info packets every 250 miliseconds. The service will stop sending 
telemetry_info packets as soon as a *disconnect* command is received. This is an example of telemetry_info packet:

```
{
    'lat': 41.124567,
    'lon': 1.9889145,
    'heading': 270,
    'groundSpeed': 4.27,
    'altitude': 6.78,
    'battery': 80,
    'state': state
}
```
The packet includes the state of the autopilot so that the module that receives the packet can take decisions (for instance, change color of the buttons).   

These are the different values for the state:
*'connected'*  
*'arming'*  
*'armed'*   
*'disarmed'*    
*'takingOff'*      
*'flying'*   
*'returningHome'*     
*'landing'*    
*'onHearth'*    

Note 2    
The state will change to *arming* and then to *armed* as soon as the autopilot is armed.    
   
   
Note 3    
The state will change to *takingOff* and then to *flying* as soon as the autopilot reaches 5 meters of altitude.  
   
Note 4    
The state will change to *returningHome* and then to *onHearth* as soon as the autopilot in on hearth.    
   
Note 5    
The state will change to *landing* and then to *onHearth* as soon as the autopilot in on hearth.    
   
Note 6    
The state will change to *disarmed*.   

Note 7     
The service must receive a json object specifying the flight plan with indications whether a picture must be taken when reaching a waypoint. This is an example of such json object:    


```
[
  {
    'lat': 41.124567,
    'lon': 1.9889145,
    'takePic': True or False
  },
  {
    'lat': 41.124567,
    'lon': 1.9889145,
    'takePic': True or False
  },
  ....
]
```
The service will execute the flight plan, changing the state accordingly (*'arming'*, *'armed'*, *'takingOff'*, and so on until *'onHearth'*).    
When arrived to the next waypoint the service will publish this message: *'XXXX/autopilotService/waypointReached'*,, being XXXX the module requesting the service. The topic of the message is a json object containing *'lat'* and *'lon'* of the reached waypoint. If a picture must be taken in this waypoint, the service will publish this message IN THE INTERNAL BROKER: *'XXXX/cameraService/takePicture'*. The autopilot will return to launch after the last waypoint is reached.   



