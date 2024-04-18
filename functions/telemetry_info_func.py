import json
import threading
import time
from pymavlink import mavutil


def get_telemetry_info(self):
    telemetry_info = {
        'lat': self.vehicle.location.global_frame.lat,
        'lon': self.vehicle.location.global_frame.lon,
        'heading': self.vehicle.heading,
        'groundSpeed': self.vehicle.groundspeed,
        'altitude': self.vehicle.location.global_relative_frame.alt,
        'battery': self.vehicle.battery.level,
        'state': self.state
    }
    return telemetry_info



def send_telemetry_info_trigger(self, external_client, internal_client, sending_topic, callback):
    self.sending_telemetry_info = True
    y = threading.Thread(target=self.send_telemetry_info_MAVLINK, args=[sending_topic, callback])
    y.start()

def send_telemetry_info_MAVLINK(self, sending_topic, callback):
    print('- Autopilot Service: Telemetry info sending started')
    frequency_hz = 2
    self.vehicle.mav.command_long_send(
        self.vehicle.target_system,  self.vehicle.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, # The MAVLink message ID (position)
        1e6 / frequency_hz, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 0, 0, 0, # Unused parameters
        0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
    )
    self.vehicle.mav.command_long_send(
        self.vehicle.target_system,  self.vehicle.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        mavutil.mavlink.MAVLINK_MSG_ID_BATTERY_STATUS, # The MAVLink message ID (battery)
        1e6 / frequency_hz, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 0, 0, 0, # Unused parameters
        0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
    )

    while self.state != 'desconectado' and self.sending_telemetry_info:
    #msg = self.vehicle.recv_match(type='AHRS2', blocking= True).to_dict()
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking= False)
        # Get battery information
        msg_battery = self.vehicle.recv_match(type='BATTERY_STATUS', blocking= False)
        if msg and msg_battery:
            msg = msg.to_dict()
            msg_battery = msg_battery.to_dict()
            self.lat = float(msg['lat'] / 10 ** 7)
            self.lon = float(msg['lon'] / 10 ** 7)
            self.alt = float(msg['relative_alt']/1000)
            self.heading = float(msg['hdg']/100)
            self.groundSpeed = float(msg['vx']/100)
            self.battery = float(msg_battery['battery_remaining'])
            telemetry_info = {
                'lat': self.lat,
                'lon': self.lon,
                'heading': self.heading,
                'groundSpeed': self.groundSpeed,
                'altitude': self.alt,
                'battery': self.battery,
                'state': self.state
            }
            # Send telemetry info using the apropiate method
            self.lock.acquire()
            callback(telemetry_info, self.ID)
            #self.external_client.publish(sending_topic + '/telemetryInfo', json.dumps(telemetry_info))
            self.lock.release()
        time.sleep(0.25)


'''
def send_output(self, data, callback):
    # This function gets the output data, process it and sends it using the callback function
    if data is not None:
        callback(data)
    else:
        print ('No output data received')
'''