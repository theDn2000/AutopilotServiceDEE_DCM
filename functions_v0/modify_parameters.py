import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil


def modify_parameter(self, param_name, param_value):
    # Change the parameter value
    self.vehicle.parameters[param_name] = param_value


def get_parameter(self, param_name):
    # Print the value of the THR_MIN parameter.
    return self.vehicle.parameters[param_name]
    print("Param: %s" % self.vehicle.parameters[param_name])
