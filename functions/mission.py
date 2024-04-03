import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil
import pymavlink.mavutil as utility

import json
import time

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
    # Open and load the waypoints file (JSON format)
    #~waypoints = json.loads(waypoints_json)
    with open(waypoints_json, 'r') as f:
        waypoints = json.load(f)

    # Print the waypoints
    print(waypoints)

    # Delete all previous missions and waypoints
    self.vehicle.mav.mission_clear_all_send(self.vehicle.target_system, self.vehicle.target_component)

    # Add as waypoints the coordinates in the JSON file
    for waypoint in waypoints['coordinates']:
        latitude = waypoint['lat']
        longitude = waypoint['lon']
        altitude = waypoint['alt']

        # Add the waypoint
        self.vehicle.mav.mission_item_send(self.vehicle.target_system, self.vehicle.target_component, 0, 0, 16, 0, 0, 0, 0, 0, latitude, longitude, altitude)

    # Upload and send feedback to the user
    self.vehicle.mav.mission_set_current_send(self.vehicle.target_system, self.vehicle.target_component, 0)
    print('Flight plan uploaded')
    return True
    
def executeFlightPlan(self):
    '''
    Execute a flight plan uploaded previously
    '''
    # The vehicle should be already connected and armed
    if self.state != 'armed':
        print('Vehicle is not armed')
        return False

    else:
        # Start the mission
        self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component, mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0)

        # Send feedback to the user
        print('Flight plan executed')
        return True