import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil
import pymavlink.mavutil as utility

import json
import time
import math

def uploadFlightPlan(self, waypoints_json):
    '''
    The waypoints_json parameter is a JSON string with the following format:
    {
    "coordinates": [
        {"lat": 47.6205, "lon": -122.3493, "alt": 100},  // Coordinate 1
        {"lat": 47.6153, "lon": -122.3448, "alt": 150},  // Coordinate 2
        {"lat": 47.6102, "lon": -122.3425, "alt": 200}   // Coordinate 3
    ]
    }
    '''
    # Load the JSON file
    waypoints_json = json.loads(waypoints_json)

    # Delete all previous missions and waypoints
    self.vehicle.mav.mission_clear_all_send(self.vehicle.target_system, self.vehicle.target_component)

    # Count the number of waypoints
    n = len(waypoints_json['coordinates'])

    self.vehicle.mav.mission_count_send(self.vehicle.target_system, self.vehicle.target_component, n, 0)

    # Add as waypoints the coordinates in the JSON file
    for waypoint in waypoints_json['coordinates']:
        latitude = waypoint['lat']
        longitude = waypoint['lon']
        altitude = waypoint['alt']

        # Add the waypoint
        self.vehicle.mav.mission_item_send(self.vehicle.target_system,                      # Target system
                                           self.vehicle.target_component,                   # Target component
                                           1,                                               # Sequence number
                                           mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,   # Frame
                                           mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,            # Command
                                           0,                                               # Current
                                           1,                                               # Autocontinue
                                           0,                                               # Param 1
                                           0,                                               # Param 2                  
                                           0,                                               # Param 3
                                           math.nan,                                        # Param 4
                                           latitude,                                        # Param 5 (Latitude)
                                           longitude,                                       # Param 6 (Longitude)
                                           altitude,                                        # Param 7 (Altitude)
                                           0)                                               # Mission type                                
                                            

    # Upload and send feedback to the user
    # self.vehicle.mav.mission_set_current_send(self.vehicle.target_system, self.vehicle.target_component, 0)
    print('Flight plan uploaded')
    return True
    
def executeFlightPlan(self):
    '''
    Execute a flight plan uploaded previously
    '''
    # The vehicle should be in auto mode
    '''
    mode_id = self.vehicle.mode_mapping()['AUTO']
    self.vehicle.mav.set_mode_send(
        self.vehicle.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    '''

    # The vehicle should be already connected and armed
    '''
    if self.state != 'armed':
        print('Vehicle is not armed')
        return False

    else:
    '''
    # Start the mission
    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component, mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0)

    # Send feedback to the user
    print('Flight plan executed')
    return True