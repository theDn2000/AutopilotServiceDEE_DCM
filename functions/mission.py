import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil
import pymavlink.mavutil as utility

import json
import time
import math

def uploadFlightPlan(self, waypoints_json):
    '''
    A mission is a set of waypoints that the vehicle will follow, from taking off to landing. 
    This function uploads a mission to the vehicle. 

    The waypoints_json parameter is a JSON string with the following format:
    {
    "coordinates": [
        {"lat": 47.6205, "lon": -122.3493, "alt": 100},  // Coordinate 1
        {"lat": 47.6153, "lon": -122.3448, "alt": 150},  // Coordinate 2
        {"lat": 47.6102, "lon": -122.3425, "alt": 200}   // Coordinate 3
    ]
    }
    '''
    waypoint_loader = []

    # Load the JSON file
    waypoints_json = json.loads(waypoints_json)

    # Count the number of waypoints
    n = len(waypoints_json['coordinates'])

    # The first waypoint is the home location, we can obtain it from the vehicle and add it to the mission
    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component, mavutil.mavlink.MAV_CMD_GET_HOME_POSITION, 0, 0, 0, 0, 0, 0, 0, 0)
    
    msg = self.vehicle.recv_match(type='HOME_POSITION', blocking=True)
    msg = msg.to_dict()
    latitude_home = msg['latitude']
    longitude_home = msg['longitude']
    altitude_home = msg['altitude']

    # Add the home waypoint to the mission
    waypoint_loader.append(utility.mavlink.MAVLink_mission_item_int_message(0,  # Target system
                                       0,                                    # Target component
                                       0,                                                                # Sequence number (0 is the home waypoint)
                                       0,                                                                # Frame
                                       16,                                                               # Command
                                       0,                                                                # Current
                                       0,                                                                # Autocontinue
                                       0,                                                                # Param 1
                                       0,                                                                # Param 2
                                       0,                                                                # Param 3
                                       0,                                                                # Param 4
                                       latitude_home,                                                    # Param 5 (Latitude)
                                       longitude_home,                                                   # Param 6 (Longitude)
                                       altitude_home))                                                   # Param 7 (Altitude)

    # Add the takeoff waypoint to the mission
    waypoint_loader.append(utility.mavlink.MAVLink_mission_item_int_message(self.vehicle.target_system,   # Target system
                                        self.vehicle.target_component,                                    # Target component
                                        1,                                                                # Sequence number (1 is the takeoff waypoint)
                                        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,                    # Frame
                                        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,                              # Command
                                        0,                                                                # Current
                                        True,                                                             # Autocontinue
                                        0,                                                                # Param 1
                                        0,                                                                # Param 2
                                        0,                                                                # Param 3
                                        0,                                                                # Param 4
                                        latitude_home,                                                    # Param 5 (Latitude)
                                        longitude_home,                                                   # Param 6 (Longitude)
                                        10))                                                              # Param 7 (Altitude)

    # Add the route waypoints to the mission
    sequence = 2
    for waypoint in waypoints_json['coordinates']:
        latitude = int(waypoint['lat']*10**7)
        longitude = int(waypoint['lon']*10**7)
        altitude = int(waypoint['alt'])

        # Add the waypoint
        waypoint_loader.append(utility.mavlink.MAVLink_mission_item_int_message(self.vehicle.target_system,  # Target system
                                           self.vehicle.target_component,                                    # Target component
                                           sequence,                                                         # Sequence number
                                           mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,                    # Frame
                                           mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,                             # Command
                                           0,                                                                # Current
                                           True,                                                             # Autocontinue
                                           0,                                                                # Param 1
                                           0,                                                                # Param 2
                                           0,                                                                # Param 3
                                           0,                                                                # Param 4
                                           latitude,                                                         # Param 5 (Latitude)
                                           longitude,                                                        # Param 6 (Longitude)
                                           altitude))                                                        # Param 7 (Altitude)
        sequence += 1

    # Add a RTL command to the mission to end the mission
    waypoint_loader.append(utility.mavlink.MAVLink_mission_item_int_message(self.vehicle.target_system,   # Target system
                                        self.vehicle.target_component,                                    # Target component
                                        sequence,                                                         # Sequence number
                                        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,                    # Frame
                                        mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,                     # Command
                                        0,                                                                # Current
                                        True,                                                             # Autocontinue
                                        0,                                                                # Param 1
                                        0,                                                                # Param 2
                                        0,                                                                # Param 3
                                        0,                                                                # Param 4
                                        0,                                                                # Param 5 (Latitude)
                                        0,                                                                # Param 6 (Longitude)
                                        0))                                                               # Param 7 (Altitude)

    # Delete all previous missions and waypoints
    self.vehicle.mav.mission_clear_all_send(self.vehicle.target_system, self.vehicle.target_component)
    
    # Recieve the ACK
    ack = self.vehicle.recv_match(type='MISSION_ACK', blocking=True)

    # Send the number of waypoints
    self.vehicle.waypoint_count_send(len(waypoint_loader))

    # Send all the items
    for i in range(0, len(waypoint_loader)):
        print("Waiting for response...")
        
        msg = self.vehicle.recv_match(type=['MISSION_REQUEST_INT', 'MISSION_REQUEST'], blocking=True)
        
        print(f'Sending waypoint {msg.seq}/{len(waypoint_loader) - 1}: {waypoint_loader[msg.seq]}')
        msg_sent = self.vehicle.mav.send(waypoint_loader[msg.seq])
        # Wait 2 seconds before sending the next waypoint
        time.sleep(2)
        print(msg_sent)


        # Break the loop if the last waypoint was sent´
        if msg.seq == len(waypoint_loader) - 1:
            break
                                        
    # Wait for the ACK
    ack = self.vehicle.recv_match(type='MISSION_ACK', blocking=True)

    # Send feedback to the user
    print('Flight plan uploaded!')
    
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

    # Wait for the ACK
    ack = self.vehicle.recv_match(type='MISSION_ACK', blocking=True)
    print(str(ack))

    # Send feedback to the user
    print('Flight plan executed')
    return True