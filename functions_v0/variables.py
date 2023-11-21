# variables.py
global state
state = 'disconnected'

global sending_telemetry_info
sending_telemetry_info = False

global vehicle
vehicle = object

global go
go = False

global direction
direction = 'Stop'


def init():
    global state
    state = 'disconnected'

    global sending_telemetry_info
    sending_telemetry_info = False

    global vehicle
    vehicle = object

# class cls_variables:
#   def __init__(self):
#      self.state = 'disconnected'
#     self.sending_telemetry_info = False
#    self.vehicle = object

#  def get_state(cls):
#     return cls.state

# def update_state(cls, new_state):
#   cls.state = new_state
