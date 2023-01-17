# Autopilot service  

## Introduction

The autopilot service is an on-board module that controls the operation of the flight controller, as required by the rest of modules in the Drone Engineering Ecosystem.   
Dashboard or mobile applications will requiere the autopilot service to connect to the flight controller, to arm the drone, take-off, go to a certain position or move in a given direction, land, stop, etc. See the table bellow for a complete list of commands that can be accepted by the autopilot service in its current version.

## Operation modes
The autopilot service can be run in simulation mode. In this case, clone the repo in your computer and install de requirements. Be also sure that you have running the internal broker at "localhost:1884". To run the service you must edit the run/debug configuration in PyCharm, as shown in the image, in order to pass the required arguments to the script (in the example of the figure the service in run in global and simulation modes).   
![autopilotConf](https://user-images.githubusercontent.com/100842082/210065804-fd15e4d0-2974-407e-b086-c443d328eaeb.png)
   
To run the autopilot service in production mode you will need the boot.py script that you will find in the main repo of the Drone Engineering Ecosystem. Follow the instruction that you will find in that repo.   

## Commands
In order to send a command to the autopilot service, a module must publish a message in the external (or internal) broker. The topic of the message must be in the form:
```
"XXX/autopilotService/YYY"
```
where XXX is the name of the module requiring the service and YYY is the name of the service that is required. Oviously, some of the commands include data that must be includes in the payload of the message to be published. 
In some cases, after completing the service requiered the autopilot service publish a message as an answer. The topic of the answer has the format:
```
"autopilotService/XXX/ZZZ"
```
where XXX is the name of the module requiring the service and ZZZ is the answer. The message can include data in the message payload.

The table bellow indicates all the commands that are accepted by the autopilot service in the current version.   

Command | Description | Payload | Answer | Answer payload
--- | --- | --- | --- |--- 
*connect* | connect with the simulator or the flight controller depending on the operation mode | No | NO (see Note 1) | No
*armDron* | arms the drone (either simulated or real) | No | NO (see Note 2) | No 
*takeOff* | get the drone take off | No | NO (see Note 2)  | No 
*returnToLaunch* | go to launch position |No  | NO (see Note 2) | No 
*disarmDrone* | disarm the drone |No  |  NO (see Note 2) | No 
*go* | move in certain direction |"North", "South", "East", "West", "NorthWest", "NorthEast", "SouthWest", "SouthEast" , "Stop"  | No | No 

*disconnect* | disconnect from the simulator or the flight controller depending on the operation mode | No | NO (see Note 1) | No


Note 1    
When the autopilot is connected the service will start sending telemetry_info packets every 250 miliseconds. This is an example of telemetry_info packet:

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
The packet includes the state of the autopilot so that the module that receive the packet can take decisions (for instance, change color of the buttons).   

These are the different values for the state:
*'connected'*  
*'arming'*  
*'armed'* 
*'takingOff'*   
*'flying'*   
*'returningHome'*   
*'landing'*
*'onHearth'*



