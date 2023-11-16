import json
import threading
import time

import AutopilotServiceDEE_DCM.AutopilotService
from AutopilotServiceDEE_DCM.AutopilotService import sending_telemetry_info # noqa: F401
from AutopilotServiceDEE_DCM.functions_v0.get_telemetry_info_v0_func import get_telemetry_info

from dronekit import connect, Command, VehicleMode

def send_telemetry_info(external_client, internal_client, sending_topic, vehicle):
    global sending_telemetry_info

    while AutopilotServiceDEE_DCM.AutopilotService.sending_telemetry_info:
        external_client.publish(sending_topic + "/telemetryInfo", json.dumps(get_telemetry_info(vehicle)))
        time.sleep(0.25)
