import json
import threading
import time

import AutopilotServiceDEE_DCM.AutopilotService
from AutopilotServiceDEE_DCM.functions_v0.get_telemetry_info_v0_func import get_telemetry_info


def send_telemetry_info_trigger(external_client, internal_client, sending_topic):
    print(AutopilotServiceDEE_DCM.functions_v0.variables.state)
    AutopilotServiceDEE_DCM.functions_v0.variables.sending_telemetry_info = True
    y = threading.Thread(target=send_telemetry_info_v0, args=[external_client, internal_client, sending_topic])
    y.start()
def send_telemetry_info_v0(external_client, internal_client, sending_topic):
    global sending_telemetry_info

    while AutopilotServiceDEE_DCM.functions_v0.variables.sending_telemetry_info:
        external_client.publish(sending_topic + "/telemetryInfo", json.dumps(get_telemetry_info()))
        time.sleep(0.25)
