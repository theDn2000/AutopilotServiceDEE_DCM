import pymavlink
from pymavlink.mavutil import default_native
import pymavlink.dialects.v20.all as dialect
import time

def clear_GEOFence(self):
    message = dialect.MAVLink_mission_clear_all_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        mission_type=dialect.MAV_MISSION_TYPE_FENCE)
    self.mav.mav.send(message)

    def upload_GEOFence(self, fence_list):
        FENCE_TOTAL = "FENCE_TOTAL".encode(encoding="utf-8")
        FENCE_ACTION = "FENCE_ACTION".encode(encoding="utf-8")

        message = dialect.MAVLink_param_request_read_message(target_system=self.target_system,
                                                             target_component=self.target_component,
                                                             param_id=FENCE_ACTION, param_index=-1)
        self.mav.mav.send(message)

        while True:
            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()

            if message["param_id"] == "FENCE_ACTION":
                fence_action_original = int(message["param_value"])
                break

        while True:
            message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        param_id=FENCE_ACTION, param_value=dialect.FENCE_ACTION_NONE,
                                                        param_type=dialect.MAV_PARAM_TYPE_REAL32)
            self.mav.mav.send(message)

            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()

            if message["param_id"] == "FENCE_ACTION":
                if int(message["param_value"]) == dialect.FENCE_ACTION_NONE:
                    break

        while True:
            message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        param_id=FENCE_TOTAL, param_value=0,
                                                        param_type=dialect.MAV_PARAM_TYPE_REAL32)
            self.mav.mav.send(message)
            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()

            if message["param_id"] == "FENCE_TOTAL":
                if int(message["param_value"]) == 0:
                    break

        while True:
            message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        param_id=FENCE_TOTAL, param_value=len(fence_list),
                                                        param_type=dialect.MAV_PARAM_TYPE_REAL32)
            self.mav.mav.send(message)
            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()

            if message["param_id"] == "FENCE_TOTAL":
                if int(message["param_value"]) == len(fence_list):
                    break

        idx = 0

        while idx < len(fence_list):
            message = dialect.MAVLink_fence_point_message(target_system=self.target_system,
                                                          target_component=self.target_component,
                                                          idx=idx, count=len(fence_list), lat=fence_list[idx][0],
                                                          lng=fence_list[idx][1])
            self.mav.mav.send(message)

            message = dialect.MAVLink_fence_fetch_point_message(target_system=self.target_system,
                                                                target_component=self.target_component, idx=idx)

            self.mav.mav.send(message)

            message = self.mav.recv_match(type="FENCE_POINT", blocking=True)
            message = message.to_dict()

            latitude = message["lat"]
            longitude = message["lng"]

            if latitude != 0.0 and longitude != 0.0:
                idx += 1

        while True:
            message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        param_id=FENCE_ACTION,
                                                        param_value=fence_action_original,
                                                        param_type=dialect.MAV_PARAM_TYPE_REAL32)
            #dialect.F
            self.mav.mav.send(message)
            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()
            if message["param_id"] == "FENCE_ACTION":
                if int(message["param_value"]) == fence_action_original:
                    break

class vehicle:
    def __init__(self, device, baud, source_system, source_component,
                 planner_format, write, append,
                 robust_parsing, notimestamps, input,
                 dialect, autoreconnect, zero_time_base,
                 retries, use_native,
                 force_connected, progress_callback,
                 udp_timeout, **opts):
        self.mav = pymavlink.mavutil.mavlink_connection(device, baud, source_system, source_component,
                                              planner_format, write, append,
                                              robust_parsing, notimestamps, input,
                                              dialect, autoreconnect, zero_time_base,
                                              retries, use_native,
                                              force_connected, progress_callback,
                                              udp_timeout, **opts)
        self.mav.wait_heartbeat()
        self.armable = False

    @property
    def target_system(self):
        return self.mav.target_system

    @property
    def target_component(self):
        return self.mav.target_component

    def command_long_send(self, CMD, confirm=0, param1=0, param2=0, param3=0, param4=0, param5=0, param6=0, param7=0):
        message = dialect.MAVLink_command_long_message(target_system=self.target_system,
                                                       target_component=self.target_component, command=CMD,
                                                       confirmation=confirm, param1=param1, param2=param2,
                                                       param3=param3, param4=param4, param5=param5, param6=param6,
                                                       param7=param7)

        self.mav.mav.send(message)
    def setmode(self, mode):
        flight_modes = self.mav.mode_mapping()
        if mode not in flight_modes.keys():
            return False
        self.command_long_send(CMD=dialect.MAV_CMD_DO_SET_MODE, param1=dialect.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                               param2=flight_modes[mode])
        return True

    def upload_GEOFence(self, fence_list):
        FENCE_TOTAL = "FENCE_TOTAL".encode(encoding="utf-8")
        FENCE_ACTION = "FENCE_ACTION".encode(encoding="utf-8")

        message = dialect.MAVLink_param_request_read_message(target_system=self.target_system,
                                                             target_component=self.target_component,
                                                             param_id=FENCE_ACTION, param_index=-1)
        self.mav.mav.send(message)

        while True:
            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()

            if message["param_id"] == "FENCE_ACTION":
                fence_action_original = int(message["param_value"])
                break

        while True:
            message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        param_id=FENCE_ACTION, param_value=dialect.FENCE_ACTION_NONE,
                                                        param_type=dialect.MAV_PARAM_TYPE_REAL32)
            self.mav.mav.send(message)

            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()

            if message["param_id"] == "FENCE_ACTION":
                if int(message["param_value"]) == dialect.FENCE_ACTION_NONE:
                    break

        while True:
            message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        param_id=FENCE_TOTAL, param_value=0,
                                                        param_type=dialect.MAV_PARAM_TYPE_REAL32)
            self.mav.mav.send(message)
            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()

            if message["param_id"] == "FENCE_TOTAL":
                if int(message["param_value"]) == 0:
                    break

        while True:
            message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        param_id=FENCE_TOTAL, param_value=len(fence_list),
                                                        param_type=dialect.MAV_PARAM_TYPE_REAL32)
            self.mav.mav.send(message)
            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()

            if message["param_id"] == "FENCE_TOTAL":
                if int(message["param_value"]) == len(fence_list):
                    break

        idx = 0

        while idx < len(fence_list):
            message = dialect.MAVLink_fence_point_message(target_system=self.target_system,
                                                          target_component=self.target_component,
                                                          idx=idx, count=len(fence_list), lat=fence_list[idx][0],
                                                          lng=fence_list[idx][1])
            self.mav.mav.send(message)

            message = dialect.MAVLink_fence_fetch_point_message(target_system=self.target_system,
                                                                target_component=self.target_component, idx=idx)

            self.mav.mav.send(message)

            message = self.mav.recv_match(type="FENCE_POINT", blocking=True)
            message = message.to_dict()

            latitude = message["lat"]
            longitude = message["lng"]

            if latitude != 0.0 and longitude != 0.0:
                idx += 1

        while True:
            message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        param_id=FENCE_ACTION,
                                                        param_value=fence_action_original,
                                                        param_type=dialect.MAV_PARAM_TYPE_REAL32)
            #dialect.F
            self.mav.mav.send(message)
            message = self.mav.recv_match(type="PARAM_VALUE", blocking=True)
            message = message.to_dict()
            if message["param_id"] == "FENCE_ACTION":
                if int(message["param_value"]) == fence_action_original:
                    break

    def clear_GEOFence(self):
        message = dialect.MAVLink_mission_clear_all_message(target_system=self.target_system,
                                                            target_component=self.target_component,
                                                            mission_type=dialect.MAV_MISSION_TYPE_FENCE)
        self.mav.mav.send(message)

    def enable_GEOFence(self, en_dis):
        if en_dis == "ENABLE":
            self.command_long_send(CMD=dialect.MAV_CMD_DO_FENCE_ENABLE, param1=1)
        else:
            self.command_long_send(CMD=dialect.MAV_CMD_DO_FENCE_ENABLE, param1=0)
