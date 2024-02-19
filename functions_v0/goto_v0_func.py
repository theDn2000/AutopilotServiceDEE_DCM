import json
import math
import threading
import time
import dronekit  # noqa: F401
from pymavlink import mavutil
from dronekit import connect, Command, VehicleMode  # noqa: F401


def goto_trigger(self, internal_client, external_client, sending_topic):
    print('- Autopilot Service: Going to the waypoint')
    self.reaching_waypoint = True
    lat = -35.3622286
    lon = 149.1650999
    w = threading.Thread(target=self.goto_MAVLINK, args=[lat, lon, internal_client, external_client, sending_topic])
    w.start()

def goto_MAVLINK(self, lat, lon, alt, sending_topic):
    self.vehicle.mav.send(
        mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, self.vehicle.target_system,
                                                                       self.vehicle.target_component,
                                                                       mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                                                       int(0b110111111000), int(lat * 10 ** 7),
                                                                       int(lon * 10 ** 7), alt, 0, 0, 0, 0, 0, 0, 0,
                                                                       0))



    dist = self._distanceToDestinationInMeters(lat ,lon)
    distanceThreshold = 0.5
    while dist > distanceThreshold:
        time.sleep(0.25)
        dist = self._distanceToDestinationInMeters(lat, lon)
    self.lock.acquire()
    self.client.publish(sending_topic + '/arrivedToPoint')
    self.lock.release()



def distanceInMeters(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5
