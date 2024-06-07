# DroneLink EETAC 

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
>This video show an example of how you can contribute to the project>\
>\
>[![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-contributions-pink.svg)](https://www.youtube.com/watch?v=dv-k5MKjq8g) 


   
## Documentation


### DroneLink EETAC

### CameraLink EETAC





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



