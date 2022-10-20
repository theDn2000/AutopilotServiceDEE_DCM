# Drone Engineering Ecosystem   
![software-arch](https://user-images.githubusercontent.com/32190349/155320787-f8549148-3c93-448b-b79a-388623ca5d3f.png)

## Demo   
[Drone Engineering Ecosystem demo](https://www.youtube.com/playlist?list=PL64O0POFYjHpXyP-T063RdKRJXuhqgaXY)   

## AutopilotController

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