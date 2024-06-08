# DroneLink EETAC 

![logo](https://github.com/theDn2000/AutopilotServiceDEE_DCM/assets/109517814/18cc8967-327c-48f8-9cfc-2be24e8043ab)

## 📋 Content table
- [Introduction](#Introduction)
- [Installation](#Installation)
- [Contributions](#Contributions)
- [Use](#Use)
- [Examples](#Examples)

<a name="Introduction"></a>
## 📄 Introduction

**DroneLink EETAC** is a project designed to facilitate interaction with drones via the MAVLink protocol, providing robustness and scalability in controlling the autopilot and its cameras. This repository includes the main library **DroneLink EETAC**, an additional library for camera control called **CameraLink EETAC**, and three practical examples that demonstrate its versatility and application potential.

>[!NOTE]
>DroneLink EETAC is a complementary module of the Drone Engineering Ecosystem, a repository from the Castelldefels School of Telecommunications and Aerospace Engineering (EETAC).\
>\
> [![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-MainRepo-brightgreen.svg)](https://github.com/dronsEETAC/DroneEngineeringEcosystemDEE)

In this file, you will find both installation instructions and a guide for using the libraries, as well as information on the operation and features of the examples.

<a name="Installation"></a>
## 📦 Installation and Requirements

>[!CAUTION]
>Before installing the project, make sure you have **Python 3.7 or higher**, which is essential for running the libraries. You can download it from [here](https://www.python.org/downloads/)

Clone the repository to your local machine using Git:

```
git clone https://github.com/tu-usuario/tu-proyecto.git A MODIFICAR
cd DroneLink-EETAC
```

Once you have the repository, download the dependencies from the *requirements.txt* file.

```
pip install -r requirements.txt
```

With this, you will be ready to use both the DroneLink EETAC library and the CameraLink EETAC library.

>[!WARNING]
>If you also want to use the examples included in this repository, you will need to have the latest version of the following tools:
>- **Mission Planner**: Essential for running the applications included in simulation mode. You can download it from [MissionPlanner](https://ardupilot.org/planner/docs/mission-planner-installation.html).
>- **Eclipse Mosquitto**: Broker required for the remote example in simulation mode. You can download it from [Mosquitto](https://mosquitto.org/download/)

<a name="Contributions"></a>
## 🤝 Contributions

This project is intended to grow from contributions both from the school and external sources. If you wish to contribute, follow the instructions below:

1. **Fork** the original repository:

   - Navigate to the [project's main page on GitHub](https://github.com/tu-usuario/tu-proyecto). A MODIFICAR
   - Click on the "Fork" button in the top right corner of the page.
   - This will create a copy of the repository in your GitHub account.
  
2. **Clone** your fork to your local machine:

   ```
   git clone https://github.com/tu-usuario-fork/tu-proyecto.git A MODIFICAR
   cd tu-proyecto
   ```

3. **Download** the dependencies from the *requirements.txt* file:
   ```
    pip install -r requirements.txt
    ```

4. Set up the original repository as an additional remote called **upstream**:

   ```
   git remote add upstream https://github.com/tu-usuario/tu-proyecto.git A MODIFICAR
   ```

5. Create a new **branch** to work on your version:

   ```
    git checkout -b nombre-de-tu-rama
   ```

Now you can make pull requests from your fork, and an administrator can merge your contributions into the main repository.
   
>[!NOTE]
>This video show an example of how you can contribute to the project\
>\
>[![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-contributions-pink.svg)](https://www.youtube.com/watch?v=dv-k5MKjq8g) 

<a name="Use"></a>
## 🚀 Use

### DroneLink EETAC

To make use of the DroneLink EETAC library, you must first import the Drone class into your project. The Drone class is defined in the file Drone.py.

```
from Drone import Drone
```

Once the library is imported, you can create a Drone object to use it. To do this, you should pass it the int ***id***, which is the identificator of that specific drone.

```
drone = Drone(id)
```

>[!TIP]
>The parameter drone.id allows you to differentiate drone-type objects, which leads you to interact with multiple vehicles at the same time. See [Dashboard Direct Multiple](#Introduction) for more information.



With the Drone object created, you can call the functions of the Drone object as follows:

```
drone.function_name(parameter_1, parameter_2, etc)
```
Below is a table with all the functions available in DroneLink EETAC:

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
>In addition, the functions that allow it have an alternative version where we can choose whether we want them to be blocking or non-blocking:

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

To use the CameraLink EETAC library, you first need to import the Camera class into your project. The Camera class is defined in the file Camera.py.

```
from Camera import Camera
```

Once the library is imported, you can create a Camera object to use it. To do this, you should pass it the int ***id***, which is the identifier of that specific camera.

```
camera = Camera(id)
```

With the Camera object created, you can call the functions of the Camera object as follows:

```
camera.function_name(parameter_1, parameter_2, etc)
```
Below is a table with all the functions available in CameraLink EETAC:

Function | Description | Parameter 1 | Parameter 2 | Parameter 3 | Response
--- | --- | --- | --- | --- | ---
*take_picture* | Take a picture using the camera | No | No | No | jpg_as_text (image encoded in base64)
*start_video_stream* | Start video stream using the camera | callback (callback function to interpret every frame) | No | No | No
*stop_video_stream* | Stop video stream  | No | No | No | No

<a name="Examples"></a>
## 🛠️ Examples

### Dashboard Direct
![image](https://github.com/theDn2000/AutopilotServiceDEE_DCM/assets/109517814/60ae827a-ad67-4943-9d87-3bba951b0288)
![image](https://github.com/theDn2000/AutopilotServiceDEE_DCM/assets/109517814/15f7517a-1417-4039-bca9-9259f4c49416)

Dashboard Direct is a tool that allows you to interact with the autopilot directly. You can connect to the Mission Planner simulator or directly to the drone through three connection methods: Telemetry Radio, MAVProxy, or Raspberry Pi integrated into the vehicle.
>[!NOTE]
>Dashboard Direct creates a Drone object with the id that you select before connecting. This application combines the frontend for the user with the backend, calling directly the functions of DroneLink EETAC and CameraLink EETAC.

Dashboard Direct offer the following functionalities:
- **Basic drone controls**: Arm the drone, take off, change altitude, move, land and RTL.
- **Position and telemetry information**: Displayed drone position in map, altitude, heading, ground speed and battery.
- **Parameters tab**: Display the value of a parameter of the Autopilot, or modify it.
- **Mission tab**: Create waypoints by right-clicking on the map, upload the flight plan, execute the flight plan or clear the waypoints.
- **Geofence tab**: Create vertex points by right-clicking on the map to define a polygon, upload the polygon to the autopilot geofence, enable the geofence, disable the geofence, change the geofence action or clear the vertex points.
- **Camera display**: Take pictures or stream video using the local camera.
- **Eclipse Mosquitto**: Broker required for the remote example in simulation mode. You can download it from [Mosquitto](https://mosquitto.org/download/)



### Dashboard Direct Multiple

### Dashboard Remote + Autopilot Service + Camera Service










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



