import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil


def modify_parameter(self, param_name, param_value):
    # Change the parameter value
    self.vehicle.parameters[param_name] = param_value

def modify_parameter_MAVLINK(self, param_name, param_value):
    # Change the parameter value
    msg = self.vehicle.mav.param_set_encode(
        self.vehicle.target_system, self.vehicle.target_component,
        param_name.encode(encoding="utf-8"), param_value, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    
    self.vehicle.mav.send(msg)


def get_parameter(self, param_name):
    # Print the value of the THR_MIN parameter.
    return self.vehicle.parameters[param_name]
    print("Param: %s" % self.vehicle.parameters[param_name])

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
    
