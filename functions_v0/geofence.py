import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil
import pymavlink.mavutil as utility

import time

def geofence_trigger(self, action):

    # DEFINE SPACE (fencelist se debería establecer como un parámetro de la función geofence_trigger. Actualmente hecho así por comodidad de desarrollo y pruebas MAVLink)
    fencelist = [(-35.363925, 149.164797,), # 0th index: return point of this fence
                    (-35.363925, 149.164797,), # 1st index: same as the Nth index
                    (-35.362147, 149.164465,),
                    (-35.361924, 149.166149,),
                    (-35.363715, 149.166455,),
                    (-35.363925, 149.164797,)] # Nth index: same as the 1st index


    if action == "enable":
        self.enable_geofence(fence_list=fencelist)

    elif action == "disable":
        self.disable_geofence()

    else:
        print("- Geofence Controller: Invalid action")



def clear_Mission(self):
    self.vehicle.mav.mission_clear_all_send(self.vehicle.target_system, self.vehicle.target_component)
    print("- Geofence Controller: Previous missions and waypoints cleared successfully")

def clear_GEOFence(self):
    # Clear the fence
    # Construct the MAVLink message for FENCE_CLEAR_ALL
    msg = self.vehicle.mav.command_long_encode(
        self.vehicle.target_system,           # ID of the system to which the message is sent
        self.vehicle.target_component,        # ID of the component to which the message is sent
        mavutil.mavlink.MAV_CMD_DO_FENCE_CLEAR_ALL,  # Command to clear all geofences
        0,                              # Confirmation (0 for no confirmation)
        0,                              # Param1 (not used)
        0,                              # Param2 (not used)
        0,                              # Param3 (not used)
        0,                              # Param4 (not used)
        0,                              # Param5 (not used)
        0,                              # Param6 (not used)
        0                               # Param7 (not used)
    )

    # Send the MAVLink message
    self.vehicle.mav.send(msg)



def complete_disable_geofence(self):
    
    
    """
        Clear previous mission and fence points
        Set FENCE_TOTAL parameter to zero to clear the old fence
        Set FENCE_ACTION parameter to 0 to disable the fence action
        Set FENCE_ENABLE parameter to 0 to disable the geofence

        https://mavlink.io/en/messages/common.html#PARAM_REQUEST_READ
        https://mavlink.io/en/messages/common.html#PARAM_VALUE
        https://mavlink.io/en/messages/ardupilotmega.html#FENCE_POINT
        https://ardupilot.org/copter/docs/parameters.html#fence-action-fence-action
        https://ardupilot.org/copter/docs/parameters.html#fence-total-fence-polygon-point-total
    """

    # CLEAR ALL MISSIONS AND GEOFENCE
    self.clear_Mission()
    # self.clear_GEOFence()
    time.sleep(1)
    print("- Geofence Controller (1/5): Previous missions and waypoints cleared successfully")

    # FENCE_TOTAL PARAMETER TO ZERO
    while True:

        # Modify the parameter value
        self.modify_parameter_MAVLINK("FENCE_TOTAL", 0)
        # Get the parameter value
        if self.get_parameter_MAVLINK("FENCE_TOTAL") == 0:
            print("- Geofence Controller (2/5): FENCE_TOTAL reset to 0 successfully")

            # Break the loop
            break

        else :
            print("- Geofence Controller: Failed to reset FENCE_TOTAL to 0, trying again")

    # SET FENCE_ACTION PARAMETER TO 3 (BRAKE WHEN REACHING THE LIMITS)
    while True:
        
        # Modify the parameter value
        self.modify_parameter_MAVLINK("FENCE_ACTION", 0)
        # Get the parameter value
        if self.get_parameter_MAVLINK("FENCE_ACTION") == 0:
            print("- Geofence Controller (3/5): FENCE_ACTION set to value 0 successfully")

            # Break the loop
            break

        else :
            print("- Geofence Controller: Failed to set FENCE_ACTION to value 0, trying again")

    # DISABLE GEOFENCE
    if self.get_parameter_MAVLINK("FENCE_ENABLE") != 0:

        while True:
            
            # Modify the parameter value
            self.modify_parameter_MAVLINK("FENCE_ENABLE", 0)
            # Get the parameter value
            if self.get_parameter_MAVLINK("FENCE_ENABLE") == 0:
                print("- Geofence Controller (4/5): Geofence disabled successfully")

                # Break the loop
                break

            else:
                print("- Geofence Controller: Failed to disable GEOFENCE, trying again")

    else:
        # Geofence was already enabled
        print("- Geofence Controller (4/5): GEOFENCE is already disabled")

    print("- Geofence Controller (5/5): Completed!")

def complete_enable_geofence(self, fence_list):

    
    """
        Clear previous mission and fence points
        Set FENCE_ENABLE parameter to 1 to enable the geofence
        Set FENCE_TOTAL parameter to zero to clear the old fence
        Set FENCE_TOTAL parameter to length on fence list
        Send FENCE_POINT messages FENCE_TOTAL many times
        Enable the fence action (set to 3 to brake when reaching the limits)

        https://mavlink.io/en/messages/common.html#PARAM_REQUEST_READ
        https://mavlink.io/en/messages/common.html#PARAM_VALUE
        https://mavlink.io/en/messages/ardupilotmega.html#FENCE_POINT
        https://ardupilot.org/copter/docs/parameters.html#fence-action-fence-action
        https://ardupilot.org/copter/docs/parameters.html#fence-total-fence-polygon-point-total
    """

    # CLEAR ALL MISSIONS AND GEOFENCE
    self.clear_Mission()
    # self.clear_GEOFence()
    time.sleep(1)
    print("- Geofence Controller (1/7): Previous missions and waypoints cleared successfully")

    # ENABLE GEOFENCE
    if self.get_parameter_MAVLINK("FENCE_ENABLE") != 1:

        while True:
            
            # Modify the parameter value
            self.modify_parameter_MAVLINK("FENCE_ENABLE", 1)
            # Get the parameter value
            if self.get_parameter_MAVLINK("FENCE_ENABLE") == 1:
                print("- Geofence Controller (2/7): Geofence enabled successfully")

                # Break the loop
                break

            else:
                print("- Geofence Controller: Failed to enable GEOFENCE, trying again")

    else:
        # Geofence was already enabled
        print("- Geofence Controller (2/7): GEOFENCE is already enabled")

    # RESET FENCE_TOTAL PARAMETER TO ZERO
    while True:

        # Modify the parameter value
        self.modify_parameter_MAVLINK("FENCE_TOTAL", 0)
        # Get the parameter value
        if self.get_parameter_MAVLINK("FENCE_TOTAL") == 0:
            print("- Geofence Controller (3/7): FENCE_TOTAL reset to 0 successfully")

            # Break the loop
            break

        else :
            print("- Geofence Controller: Failed to reset FENCE_TOTAL to 0, trying again")

    # SET FENCE_TOTAL PARAMETER TO LENGTH OF FENCE LIST
    while True:

        # Modify the parameter value
        self.modify_parameter_MAVLINK("FENCE_TOTAL", len(fence_list))
        # Get the parameter value
        if self.get_parameter_MAVLINK("FENCE_TOTAL") == len(fence_list):
            print("- Geofence Controller (4/7): FENCE_TOTAL set to {0} successfully".format(len(fence_list)))

            # Break the loop
            break

        else :
            print("- Geofence Controller: Failed to set FENCE_TOTAL to {0}, trying again".format(len(fence_list)))

    # SET THE FENCE BY SENDING FENCE_POINT MESSAGES
    # Initialize fence item index counter
    idx = 0

    # Run until all the fence items uploaded successfully
    while idx < len(fence_list):

        # Create FENCE_POINT message
        message = dialect.MAVLink_fence_point_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    idx=idx,
                                                    count=len(fence_list),
                                                    lat=fence_list[idx][0],
                                                    lng=fence_list[idx][1])

        # Send this message to vehicle
        self.vehicle.mav.send(message)

        # Create FENCE_FETCH_POINT message (this message is used to check if the fence point is uploaded successfully)
        message = dialect.MAVLink_fence_fetch_point_message(target_system=self.vehicle.target_system,
                                                            target_component=self.vehicle.target_component,
                                                            idx=idx)

        # Send this message to vehicle
        self.vehicle.mav.send(message)

        # Wait until receive FENCE_POINT message
        message = self.vehicle.recv_match(type=dialect.MAVLink_fence_point_message.msgname,
                                    blocking=True)

        # Convert the message to dictionary
        message = message.to_dict()

        # get the latitude and longitude from the fence item
        latitude = message["lat"]
        longitude = message["lng"]

        # Check the fence point is uploaded successfully
        if latitude != 0.0 and longitude != 0:
            # Print that the fence item uploaded successfully converting to string
            print("- Geofence Controller: Fence waypoint" + str(latitude) + " " + str(longitude) + " uploaded successfully")
            # Increase the index of the fence item
            idx += 1

    print("- Geofence Controller (5/7): All the fence items uploaded successfully")


    # SET FENCE_ACTION PARAMETER TO 3 (BRAKE WHEN REACHING THE LIMITS)
    while True:
        
        # Modify the parameter value
        self.modify_parameter_MAVLINK("FENCE_ACTION", 3)
        # Get the parameter value
        if self.get_parameter_MAVLINK("FENCE_ACTION") == 3:
            print("- Geofence Controller (6/7): FENCE_ACTION set to value 3 successfully")

            # Break the loop
            break

        else :
            print("- Geofence Controller: Failed to set FENCE_ACTION to value 3, trying again")
    
    print("- Geofence Controller (7/7): Completed!")



def enable_geofence(self):




    # ENABLE GEOFENCE
    if self.get_parameter_MAVLINK("FENCE_ENABLE") != 1:

        while True:
            
            # Modify the parameter value
            self.modify_parameter_MAVLINK("FENCE_ENABLE", 1)
            # Get the parameter value
            if self.get_parameter_MAVLINK("FENCE_ENABLE") == 1:
                print("- Geofence Controller: Geofence enabled successfully")

                # Break the loop
                break

            else:
                print("- Geofence Controller: Failed to enable GEOFENCE, trying again")

    else:
        # Geofence was already enabled
        print("- Geofence Controller: GEOFENCE is already enabled")

def disable_geofence(self):
    # DISABLE GEOFENCE
    if self.get_parameter_MAVLINK("FENCE_ENABLE") != 0:

        while True:
            
            # Modify the parameter value
            self.modify_parameter_MAVLINK("FENCE_ENABLE", 0)
            # Get the parameter value
            if self.get_parameter_MAVLINK("FENCE_ENABLE") == 0:
                print("- Geofence Controller: Geofence disabled successfully")

                # Break the loop
                break

            else:
                print("- Geofence Controller: Failed to disable GEOFENCE, trying again")

    else:
        # Geofence was already enabled
        print("- Geofence Controller: GEOFENCE is already disabled")

    print("- Geofence Controller: Completed!")

def set_fence_geofence(self, fence_list):
    # SET FENCE_TOTAL PARAMETER TO LENGTH OF FENCE LIST
    while True:

        # Modify the parameter value
        self.modify_parameter_MAVLINK("FENCE_TOTAL", len(fence_list))
        # Get the parameter value
        if self.get_parameter_MAVLINK("FENCE_TOTAL") == len(fence_list):
            print("- Geofence Controller FENCE_TOTAL set to {0} successfully".format(len(fence_list)))

            # Break the loop
            break

        else :
            print("- Geofence Controller: Failed to set FENCE_TOTAL to {0}, trying again".format(len(fence_list)))

    # SET THE FENCE BY SENDING FENCE_POINT MESSAGES
    # Initialize fence item index counter
    idx = 0

    # Run until all the fence items uploaded successfully
    while idx < len(fence_list):

        # Create FENCE_POINT message
        message = dialect.MAVLink_fence_point_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    idx=idx,
                                                    count=len(fence_list),
                                                    lat=fence_list[idx][0],
                                                    lng=fence_list[idx][1])

        # Send this message to vehicle
        self.vehicle.mav.send(message)

        # Create FENCE_FETCH_POINT message (this message is used to check if the fence point is uploaded successfully)
        message = dialect.MAVLink_fence_fetch_point_message(target_system=self.vehicle.target_system,
                                                            target_component=self.vehicle.target_component,
                                                            idx=idx)

        # Send this message to vehicle
        self.vehicle.mav.send(message)

        # Wait until receive FENCE_POINT message
        message = self.vehicle.recv_match(type=dialect.MAVLink_fence_point_message.msgname,
                                    blocking=True)

        # Convert the message to dictionary
        message = message.to_dict()

        # get the latitude and longitude from the fence item
        latitude = message["lat"]
        longitude = message["lng"]

        # Check the fence point is uploaded successfully
        if latitude != 0.0 and longitude != 0:
            # Print that the fence item uploaded successfully converting to string
            print("- Geofence Controller: Fence waypoint" + str(latitude) + " " + str(longitude) + " uploaded successfully")
            # Increase the index of the fence item
            idx += 1

    print("- Geofence Controller (5/7): All the fence items uploaded successfully")

def action_geofence(self, action):
    # SET FENCE_ACTION PARAMETER
    while True:
        
        # Modify the parameter value
        self.modify_parameter_MAVLINK("FENCE_ACTION", int(action)
        # Get the parameter value
        if self.get_parameter_MAVLINK("FENCE_ACTION") == int(action):
            print("- Geofence Controller: FENCE_ACTION set to value 3 successfully")

            # Break the loop
            break

        else :
            print("- Geofence Controller: Failed to set FENCE_ACTION to value 3, trying again")
    
    print("- Geofence Controller: Completed!")












