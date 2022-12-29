# Autopilot service  

## Introduction

The autopilot service is an on-board module that controls the operation of the flight controller, as required by the rest of modules in the Drone Engineering Ecosystem.   
Dashboard or mobile applications will requiere the autopilot service to connect to the flight controller to arm the drone, take-off, go to a certain position or move in a given direction, land, stop, etc. See the table bellow for a complete list of commands that can be accepted by the autopilot service in its current version.

## Operation modes
The autopilot service can be run in simulation mode. In this case, clone the repo in your computer and install de requirements. Be also sure that you have running the internal broker at "localhost:1884". To run the service you must edit the run/debug configuration in PyCharm, as shown in the image, in order to pass the required arguments to the script (in the example of the figure the service in run in global and simulation modes).   
   
To run the autopilot service in production mode you will need the boot.py script that you will find in the main repo of the Drone Engineering Ecosystem. Follow the instruction that you will find in that repo.   

## Commands
In order to send a command to the autopilot service, a module must publish a message in the external (or internal) broker. The topic of the message must be in the form:
```
"XXX/autopilotService/YYY"
```
where XXX is the name of the module requiring the service and YYY is the name of the service that is required. Oviously, some of the commands include data that must be includes in the payload of the message to be published.   

The table bellow indicates all the commands that are accepted by the autopilot service in the current version.   

Attempt | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 | #9 | #10 | #11
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |---
Seconds | 301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269


The Autopilot does several things with the help of **dronekit** library. As well, it is linked to the local MQTT broker,
which can listen/publish different messages and do several actions with them. These are examples of what the Autopilot
is able to do:

- Connect to platform (subscribe to the autopilot service to get all the messages and connect the drone)
- Arm drone
- Take off
- Get drone heading
- Get drone position
- Get drone speed
- Make the drone go to a certain position
- Stop getting positions for the drone to go to
- Disarm drone

## Example and tutorials

The basics of MQTT can be found here:   
[MQTT](https://www.youtube.com/watch?v=EIxdz-2rhLs)

This is a good example to start using MQTT (using a public broker):    
[Example](https://www.youtube.com/watch?v=kuyCd53AOtg)
