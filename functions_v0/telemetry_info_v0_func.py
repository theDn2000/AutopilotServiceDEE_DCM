import json
import threading
import time


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


def send_telemetry_info_trigger(self, external_client, internal_client, sending_topic):
    print(self.state)
    self.sending_telemetry_info = True
    y = threading.Thread(target=self.send_telemetry_info_v0, args=[external_client, internal_client, sending_topic])
    y.start()


def send_telemetry_info_v0(self, external_client, internal_client, sending_topic):
    while self.sending_telemetry_info:
        external_client.publish(sending_topic + "/telemetryInfo", json.dumps(self.get_telemetry_info()))
        time.sleep(0.25)
