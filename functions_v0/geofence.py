import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil
import pymavlink.mavutil as utility

import time

def clear_Mission(self):
    self.vehicle.commands.clear()
    self.vehicle.commands.upload()


def clear_GEOFence(self):
    # Clear the fence
    self.vehicle.commands.clear()
    # message = self.vehicle.message_factory.mission_clear_all_encode(self.vehicle.target_system, self.vehicle.target_component, dialect.MAV_MISSION_TYPE_FENCE)
    # message = dialect.MAVLink_mission_clear_all_message(target_system=self.target_system, target_component=self.target_component, mission_type=dialect.MAV_MISSION_TYPE_FENCE)
    # self.mav.mav.send(message)

def prepare_geofence(self, fencelist):
    """
    Prepare the command to upload the geofence
    """
    for vertex in fencelist:
        lat, lon, alt = vertex
        cmd = self.vehicle.message_factory.command_long_encode(
            0,  
            0,  # target system, target component
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,  # frame
            0, # Confirmation
            0, # param 1: Hold time in decimal seconds. (ignored by fixed wing, time to stay at MISSION for rotary wing)
            0, # param 2: Acceptance radius in meters (if the sphere with this radius is hit, the MISSION counts as reached)
            0, # param 3: 0 to pass through the WP, if > 0 radius in meters to pass by WP. Positive value for clockwise orbit, negative value for counter-clockwise orbit. Allows trajectory control.
            0, # param 4: Desired yaw angle at MISSION (rotary wing)
            lat,
            lon,
            alt,  # param 5 ~ 7: X, Y, Z Waypoint coordinates
        )

        print("Sending waypoint %s" % cmd)
        # return cmd
        self.vehicle.commands.add(cmd)

    # Configure Geofence to brake when trespassing
    self.vehicle.parameters['FENCE_ACTION'] = 3

    # Upload the geofence
    self.vehicle.commands.upload()


def upload_GEOFence(self, fence_list):
    FENCE_TOTAL = "FENCE_TOTAL".encode(encoding="utf-8")
    FENCE_ACTION = "FENCE_ACTION".encode(encoding="utf-8")

    message = dialect.MAVLink_param_request_read_message(target_system=self.target_system,
                                                         target_component=self.target_component,
                                                         param_id=FENCE_ACTION, param_index=-1)
    self.mav.mav.send(message)

    while True:
        message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()

        if message["param_id"] == "FENCE_ACTION":
            fence_action_original = int(message["param_value"])
            break

    while True:
        message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                    target_component=self.target_component,
                                                    param_id=FENCE_ACTION, param_value=dialect.FENCE_ACTION_NONE,
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)
        self.mav.mav.send(message)

        message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()

        if message["param_id"] == "FENCE_ACTION":
            if int(message["param_value"]) == dialect.FENCE_ACTION_NONE:
                break

    while True:
        message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                    target_component=self.target_component,
                                                    param_id=FENCE_TOTAL, param_value=0,
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)
        self.mav.mav.send(message)
        message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()

        if message["param_id"] == "FENCE_TOTAL":
            if int(message["param_value"]) == 0:
                break

    while True:
        message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                    target_component=self.target_component,
                                                    param_id=FENCE_TOTAL, param_value=len(fence_list),
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)
        self.mav.mav.send(message)
        message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()

        if message["param_id"] == "FENCE_TOTAL":
            if int(message["param_value"]) == len(fence_list):
                break

    idx = 0

    while idx < len(fence_list):
        message = dialect.MAVLink_fence_point_message(target_system=self.target_system,
                                                      target_component=self.target_component,
                                                      idx=idx, count=len(fence_list), lat=fence_list[idx][0],
                                                      lng=fence_list[idx][1])
        self.mav.mav.send(message)

        message = dialect.MAVLink_fence_fetch_point_message(target_system=self.target_system,
                                                            target_component=self.target_component, idx=idx)

        self.mav.mav.send(message)

        message = self.mav.recv_match(type="FENCE_POINT", blocking=True)
        message = message.to_dict()

        latitude = message["lat"]
        longitude = message["lng"]

        if latitude != 0.0 and longitude != 0.0:
            idx += 1

    while True:
        message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                    target_component=self.target_component,
                                                    param_id=FENCE_ACTION,
                                                    param_value=fence_action_original,
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)
        # dialect.F
        self.mav.mav.send(message)
        message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()
        if message["param_id"] == "FENCE_ACTION":
            if int(message["param_value"]) == fence_action_original:
                break

    self.vehicle.setparam('FENCE_ALT_MAX', 58)
    self.vehicle.setparam('FENCE_ENABLE', 1)


# ESTA FUNCIÓN ACTUALMENTE ESTÁ INCACTIVA
def command_long_send(self, command, confirm=0, param1=0, param2=0, param3=0, param4=0, param5=0, param6=0, param7=0):
    #message = mavutil.mavlink.MAVLink_command_long_message(target_system=self.vehicle.system_id,
                                                   #target_component=mavutil.mavlink.MAV_COMPONENT_ID_ALL, command=command,
                                                   #confirmation=confirm, param1=param1, param2=param2,
                                                   #param3=param3, param4=param4, param5=param5, param6=param6,
                                                   #param7=param7)
    self.vehicle.send_mavlink("COMMAND_LONG", 0, 0, command, 0, param1, param2, param3, param4, param5, param6, param7)


def set_geofence(self, fence_list):
    """
    Get vehicle's FENCE_ACTION parameter
    Disable the fence action (set FENCE_ACTION parameter to zero)
    Set FENCE_TOTAL parameter to zero to clear the old fence
    Set FENCE_TOTAL parameter to length on fence list
    Send FENCE_POINT messages FENCE_TOTAL many times
    Enable the fence action (set to original value)

    https://mavlink.io/en/messages/common.html#PARAM_REQUEST_READ
    https://mavlink.io/en/messages/common.html#PARAM_VALUE
    https://mavlink.io/en/messages/ardupilotmega.html#FENCE_POINT
    https://ardupilot.org/copter/docs/parameters.html#fence-action-fence-action
    https://ardupilot.org/copter/docs/parameters.html#fence-total-fence-polygon-point-total
    """

    # introduce FENCE_TOTAL and FENCE_ACTION as byte array and do not use parameter index
    FENCE_TOTAL = "FENCE_TOTAL".encode(encoding="utf-8")
    FENCE_ACTION = "FENCE_ACTION".encode(encoding="utf8")
    PARAM_INDEX = -1

    # THE VEHICLE IS ALREADY CONNECTED, SO WE DO NOT NEED TO CONNECT AGAIN
    # connect to vehicle
    # vehicle = utility.mavlink_connection(device="udpin:127.0.0.1:14560")

    # wait for a heartbeat
    # self.vehicle.wait_ready()

    # inform user
    print("Connected to system:", 0, ", component:", 0)

    # RESET FENCE_ACTION
    self.vehicle.parameters["FENCE_ACTION"] = -1

    # RESET FENCE_TOTAL
    while True:

        # reset FENCE_TOTAL parameter to zero
        self.vehicle.parameters["FENCE_TOTAL"] = 0

        # make sure that parameter value set successfully
        if int(self.vehicle.parameters["FENCE_TOTAL"]) == 0:
            print("FENCE_TOTAL reset to 0 successfully")

            # break the loop
            break

        # should send param reset message again
        else:
            print("Failed to reset FENCE_TOTAL to 0, trying again")

    # SET FENCE_TOTAL
    while True:

        # reset FENCE_TOTAL parameter to zero
        self.vehicle.parameters["FENCE_TOTAL"] = len(fence_list)

        # make sure that parameter value set successfully
        if int(self.vehicle.parameters["FENCE_TOTAL"]) == len(fence_list):
            print("FENCE_TOTAL set to {0} successfully".format(len(fence_list)))

            # break the loop
            break

        # should send param reset message again
        else:
            print("Failed to reset FENCE_TOTAL to {0}, trying again".format(len(fence_list)))

    # SET FENCE_ALT_MAX
    while True:

        # reset FENCE_TOTAL parameter to zero
        self.vehicle.parameters["FENCE_ALT_MAX"] = 10

        # make sure that parameter value set successfully
        if self.vehicle.parameters["FENCE_ALT_MAX"] == 10:
            print("FENCE_ALT_MAX set to 10 meters successfully")

            # break the loop
            break

        # should send param reset message again
        else:
            print("Failed to set FENCE_ALT_MAX to 10 meters, trying again")
    # initialize fence item index counter
    idx = 0

    # run until all the fence items uploaded successfully
    while idx < len(fence_list):

        # create FENCE_POINT message
        message = dialect.MAVLink_fence_point_message(target_system=0,
                                                    target_component=0,
                                                    idx=idx,
                                                    count=len(fence_list),
                                                    lat=fence_list[idx][0],
                                                    lng=fence_list[idx][1])

        # send this message to vehicle
        # self.vehicle.mav.send(message) MAV ESTÁ EN DESUSO
        self.vehicle.send_mavlink(message)

        # create FENCE_FETCH_POINT message
        message = dialect.MAVLink_fence_fetch_point_message(target_system=0,
                                                            target_component=0,
                                                            idx=idx)

        # send this message to vehicle
        # self.vehicle.mav.send(message) MAV ESTÁ EN DESUSO
        self.vehicle.send_mavlink(message)


        # Espera recibir el mensaje específico

        # wait until receive FENCE_POINT message
        # message = self.vehicle.recv_match(type=dialect.MAVLink_fence_point_message.msgname, blocking=True)

        # convert the message to dictionary
        # message = message.to_dict()

        # get the latitude and longitude from the fence item
        # latitude = message["lat"]
        # longitude = message["lng"]

        # check the fence point is uploaded successfully
        # if latitude != 0.0 and longitude != 0:
            # increase the index of the fence item
        idx += 1

    print("All the fence items uploaded successfully")

    # EN EL SCRIPT CONSULTADO, AL FINAL RESETEA EL VALOR DE FENCE ACTION A SU VALOR ORIGINAL

    # SET FENCE_ACTION
    while True:

        self.vehicle.parameters["FENCE_ACTION"] = 3

        # make sure that parameter value reset successfully
        if int(self.vehicle.parameters["FENCE_ACTION"]) == 3:
            print("FENCE_ACTION stabilized to 3 successfully (brake when reaching the limits)")

            # break the loop
            break

        # should send param set message again
        else:
            print("Failed to stablish FENCE_ACTION to 3 (brake when reaching the limits), trying again")


def set_geofence_MAVLINK(self, fence_list):
    
    """
        Get vehicle's FENCE_ACTION parameter
        Disable the fence action (set FENCE_ACTION parameter to zero)
        Set FENCE_TOTAL parameter to zero to clear the old fence
        Set FENCE_TOTAL parameter to length on fence list
        Send FENCE_POINT messages FENCE_TOTAL many times
        Enable the fence action (set to original value)

        https://mavlink.io/en/messages/common.html#PARAM_REQUEST_READ
        https://mavlink.io/en/messages/common.html#PARAM_VALUE
        https://mavlink.io/en/messages/ardupilotmega.html#FENCE_POINT
        https://ardupilot.org/copter/docs/parameters.html#fence-action-fence-action
        https://ardupilot.org/copter/docs/parameters.html#fence-total-fence-polygon-point-total
    """

    # introduce FENCE_TOTAL and FENCE_ACTION as byte array and do not use parameter index
    FENCE_TOTAL = "FENCE_TOTAL".encode(encoding="utf-8")
    FENCE_ACTION = "FENCE_ACTION".encode(encoding="utf8")
    PARAM_INDEX = -1

    # create PARAM_REQUEST_READ message
    message = dialect.MAVLink_param_request_read_message(target_system=self.vehicle.target_system,
                                                        target_component=self.vehicle.target_component,
                                                        param_id=FENCE_ACTION,
                                                        param_index=PARAM_INDEX)

    # send PARAM_REQUEST_READ message to the vehicle
    self.vehicle.mav.send(message)

    # wait until get FENCE_ACTION
    while True:

        # wait for PARAM_VALUE message
        message = self.vehicle.recv_match(type=dialect.MAVLink_param_value_message.msgname,
                                    blocking=True)

        # convert the message to dictionary
        message = message.to_dict()

        # make sure this parameter value message is for FENCE_ACTION
        if message["param_id"] == "FENCE_ACTION":
            # get the original fence action parameter from vehicle
            fence_action_original = int(message["param_value"])

            # break the loop
            break

    # debug parameter value
    print("FENCE_ACTION parameter original:", fence_action_original)

    # run until parameter set successfully
    while True:

        # create parameter set message
        message = dialect.MAVLink_param_set_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    param_id=FENCE_ACTION,
                                                    param_value=dialect.FENCE_ACTION_NONE,
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)

        # send parameter set message to the vehicle
        self.vehicle.mav.send(message)

        # wait for PARAM_VALUE message
        message = self.vehicle.recv_match(type=dialect.MAVLink_param_value_message.msgname,
                                    blocking=True)

        # convert the message to dictionary
        message = message.to_dict()

        # make sure this parameter value message is for FENCE_ACTION
        if message["param_id"] == "FENCE_ACTION":

            # make sure that parameter value reset successfully
            if int(message["param_value"]) == dialect.FENCE_ACTION_NONE:
                print("FENCE_ACTION reset to 0 successfully")

                # break the loop
                break

            # should send param set message again
            else:
                print("Failed to reset FENCE_ACTION to 0, trying again")

    # run until parameter reset successfully
    while True:

        # create parameter reset message
        message = dialect.MAVLink_param_set_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    param_id=FENCE_TOTAL,
                                                    param_value=0,
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)

        # send parameter reset message to the vehicle
        self.vehicle.mav.send(message)

        # wait for PARAM_VALUE message
        message = self.vehicle.recv_match(type=dialect.MAVLink_param_value_message.msgname,
                                    blocking=True)

        # convert the message to dictionary
        message = message.to_dict()

        # make sure this parameter value message is for FENCE_TOTAL
        if message["param_id"] == "FENCE_TOTAL":

            # make sure that parameter value set successfully
            if int(message["param_value"]) == 0:
                print("FENCE_TOTAL reset to 0 successfully")

                # break the loop
                break

            # should send param reset message again
            else:
                print("Failed to reset FENCE_TOTAL to 0")

    # run until parameter set successfully
    while True:

        # create parameter set message
        message = dialect.MAVLink_param_set_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    param_id=FENCE_TOTAL,
                                                    param_value=len(fence_list),
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)

        # send parameter set message to the vehicle
        self.vehicle.mav.send(message)

        # wait for PARAM_VALUE message
        message = self.vehicle.recv_match(type=dialect.MAVLink_param_value_message.msgname,
                                    blocking=True)

        # convert the message to dictionary
        message = message.to_dict()

        # make sure this parameter value message is for FENCE_TOTAL
        if message["param_id"] == "FENCE_TOTAL":

            # make sure that parameter value set successfully
            if int(message["param_value"]) == len(fence_list):
                print("FENCE_TOTAL set to {0} successfully".format(len(fence_list)))

                # break the loop
                break

            # should send param set message again
            else:
                print("Failed to set FENCE_TOTAL to {0}".format(len(fence_list)))

    # initialize fence item index counter
    idx = 0

    # run until all the fence items uploaded successfully
    while idx < len(fence_list):

        # create FENCE_POINT message
        message = dialect.MAVLink_fence_point_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    idx=idx,
                                                    count=len(fence_list),
                                                    lat=fence_list[idx][0],
                                                    lng=fence_list[idx][1])

        # send this message to vehicle
        self.vehicle.mav.send(message)

        # create FENCE_FETCH_POINT message
        message = dialect.MAVLink_fence_fetch_point_message(target_system=self.vehicle.target_system,
                                                            target_component=self.vehicle.target_component,
                                                            idx=idx)

        # send this message to vehicle
        self.vehicle.mav.send(message)

        # wait until receive FENCE_POINT message
        message = self.vehicle.recv_match(type=dialect.MAVLink_fence_point_message.msgname,
                                    blocking=True)

        # convert the message to dictionary
        message = message.to_dict()

        # get the latitude and longitude from the fence item
        latitude = message["lat"]
        longitude = message["lng"]

        # check the fence point is uploaded successfully
        if latitude != 0.0 and longitude != 0:
            # increase the index of the fence item
            idx += 1

    print("All the fence items uploaded successfully")

    # run until parameter set successfully
    while True:

        # create parameter set message
        message = dialect.MAVLink_param_set_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    param_id=FENCE_ACTION,
                                                    param_value=fence_action_original,
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)

        # send parameter set message to the vehicle
        self.vehicle.mav.send(message)

        # wait for PARAM_VALUE message
        message = self.vehicle.recv_match(type=dialect.MAVLink_param_value_message.msgname,
                                    blocking=True)

        # convert the message to dictionary
        message = message.to_dict()

        # make sure this parameter value message is for FENCE_ACTION
        if message["param_id"] == "FENCE_ACTION":

            # make sure that parameter value set successfully
            if int(message["param_value"]) == fence_action_original:
                print("FENCE_ACTION set to original value {0} successfully".format(fence_action_original))

                # break the loop
                break

            # should send param set message again
            else:
                print("Failed to set FENCE_ACTION to original value {0} ".format(fence_action_original))