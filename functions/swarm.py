import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil
import threading

def get_swarm_info(self, blocking=False):
    if blocking:
        return get_swarm_info_MAVLINK(self)
    else:
        w = threading.Thread(target=get_swarm_info_MAVLINK, args=[self])
        w.start()

def get_swarm_info_MAVLINK(self):
    while True:
        msg = self.vehicle.recv_match(type='SWARM_STATUS', blocking=True)
        print("SWARM STATUS: ", msg)
    