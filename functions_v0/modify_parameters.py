import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil


def modify_parameter(self, param_name, param_value):
    # Change the parameter value
    self.vehicle.parameters[param_name] = param_value´

def modify_parameter_MAVLINK(self, param_name, param_value):
    # Change the parameter value
    msg = self.vehicle.message_factory.param_set_encode(
        self.vehicle.target_system, self.vehicle.target_component,
        param_name, param_value, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    
    self.vehicle.send_mavlink(msg)


def get_parameter(self, param_name):
    # Print the value of the THR_MIN parameter.
    return self.vehicle.parameters[param_name]
    print("Param: %s" % self.vehicle.parameters[param_name])

def get_parameter_MAVLINK(self, param_name):
    # Print the value of the THR_MIN parameter.
    msg = self.vehicle.message_factory.param_request_read_encode(
        self.vehicle.target_system, self.vehicle.target_component,
        param_name, -1)
    
    self.vehicle.send_mavlink(msg, False, False)
    #self.vehicle.wait_heartbeat()
    print("Param: %s" % self.vehicle.parameters[param_name])
