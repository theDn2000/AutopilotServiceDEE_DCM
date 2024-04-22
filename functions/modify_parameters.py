import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil
import threading


def modify_parameter(self, param_name, param_value, blocking=False):
    if blocking:
        modify_parameter_MAVLINK(self, param_name, param_value)
    else:
        w = threading.Thread(target=modify_parameter_MAVLINK, args=[self, param_name, param_value])
        w.start()

def modify_parameter_MAVLINK(self, param_name, param_value):
    # Change the parameter value
    msg = self.vehicle.mav.param_set_encode(
        self.vehicle.target_system, self.vehicle.target_component,
        param_name.encode(encoding="utf-8"), param_value, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    
    self.vehicle.mav.send(msg)



def get_parameter(self, param_name, blocking=False):
    if blocking:
        return get_parameter_MAVLINK(self, param_name)
    else:
        w = threading.Thread(target=get_parameter_MAVLINK, args=[self, param_name])
        w.start()

def get_parameter_MAVLINK(self, param_name):
    # Print the value of the THR_MIN parameter.
    msg = self.vehicle.mav.param_request_read_encode(
        self.vehicle.target_system, self.vehicle.target_component,
        param_name.encode(encoding="utf-8"), -1)
    
    self.vehicle.mav.send(msg)

    # Wait for a response (blocking)
    response = self.vehicle.recv_match(type='PARAM_VALUE', blocking=True)
    # Return the value of the parameter
    return response.param_value
    


def  get_all_parameters(self, blocking=False):
    if blocking:
        return get_all_parameters_MAVLINK(self)
    else:
        w = threading.Thread(target=get_all_parameters_MAVLINK, args=[self])
        w.start()

def get_all_parameters_MAVLINK(self):
    # Print all parameters
    msg = self.vehicle.mav.param_request_list_encode(
        self.vehicle.target_system, mavutil.mavlink.MAV_COMP_ID_ALL)
    
    self.vehicle.mav.send(msg)

    # Create a list with all the parameters
    parameters_id = []
    parameters_value = []
    while True:
        response = self.vehicle.recv_match(type='PARAM_VALUE', blocking=True)
        if response.param_count == response.param_index + 1:

            break
        print(response.param_id, response.param_value)
        parameters_id.append(response.param_id)
        parameters_value.append(response.param_value)
    return parameters_id, parameters_value


# Función a determinar su ubicación:
def get_position(self):
    # Get the drone position, latitude, longitude and altitude
    self.vehicle.mav.mission_request_send(self.vehicle.target_system, self.vehicle.target_component, 0)

    # Wait for a response (blocking)
    msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    # Return the value of the parameter


    msg = msg.to_dict()
    latitude = msg['lat']*1e-7
    longitude = msg['lon']*1e-7
    altitude = msg['alt']*1e-3

    return latitude, longitude, altitude