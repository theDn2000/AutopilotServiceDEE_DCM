import pymavlink
from pymavlink.mavutil import default_native
import pymavlink.dialects.v20.all as dialect
import time


def connection(device, baud=115200, source_system=255, source_component=0,
               planner_format=None, write=False, append=False,
               robust_parsing=True, notimestamps=False, input=True,
               dialect=None, autoreconnect=False, zero_time_base=False,
               retries=3, use_native=default_native,
               force_connected=False, progress_callback=None,
               udp_timeout=0, **opts):
    return vehicle(device, baud, source_system, source_component,
                   planner_format, write, append,
                   robust_parsing, notimestamps, input,
                   dialect, autoreconnect, zero_time_base,
                   retries, use_native,
                   force_connected, progress_callback,
                   udp_timeout, **opts)


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

    def is_armable(self, timeout=60, interval=0.1):
        if self.armable is False:
            t0 = time.time()
            while time.time() - t0 <= timeout:
                self.command_long_send(dialect.MAV_CMD_REQUEST_MESSAGE, param1=193)
                msg = self.mav.recv_match(type='EKF_STATUS_REPORT', blocking=True)
                if (msg.flags >= 512) and (msg.flags < 1024):
                    self.armable = True
                    return True
                time.sleep(interval)

            return False
        else:
            return self.armable

    def setmode(self, mode):
        flight_modes = self.mav.mode_mapping()
        if mode not in flight_modes.keys():
            return False
        self.command_long_send(CMD=dialect.MAV_CMD_DO_SET_MODE, param1=dialect.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                               param2=flight_modes[mode])
        return True

    def arm(self):
        self.command_long_send(dialect.MAV_CMD_COMPONENT_ARM_DISARM, param1=1)
        time.sleep(0.1)
        msg = self.mav.recv_match(type='COMMAND_ACK', condition='COMMAND_ACK.command==400', blocking=True)
        if msg.result == 0:
            return "Armed"
        elif msg.result == 1:
            return "Temporarily Rejected"
        elif msg.result == 2:
            return "Denied"
        elif msg.result == 3:
            return "Unsupported"
        elif msg.result == 4:
            return "Failed"
        elif msg.result == 5:
            return "In Progress"
        elif msg.result == 6:
            return "Cancelled"
        else:
            return "Unknown"

    def takeoff(self, alt):
        self.command_long_send(dialect.MAV_CMD_NAV_TAKEOFF, param7=alt)

    def land(self):
        self.command_long_send(CMD=dialect.MAV_CMD_NAV_LAND)

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

    def upload_Mission(self, mission_list):
        self.clear_Mission()
        message = dialect.MAVLink_mission_count_message(target_system=self.target_system,
                                                        target_component=self.target_component,
                                                        count=len(mission_list) + 2,
                                                        mission_type=dialect.MAV_MISSION_TYPE_MISSION)
        self.mav.mav.send(message)

        while True:
            message = self.mav.recv_match(blocking=True)
            message = message.to_dict()

            if message["mavpackettype"] == "MISSION_REQUEST":
                if message["mission_type"] == dialect.MAV_MISSION_TYPE_MISSION:
                    seq = message["seq"]

                    if seq == 0:  # Home Location
                        message = dialect.MAVLink_mission_item_message(target_system=self.target_system,
                                                                       target_component=self.target_component,
                                                                       seq=seq, frame=dialect.MAV_FRAME_GLOBAL,
                                                                       command=dialect.MAV_CMD_NAV_WAYPOINT, current=0,
                                                                       autocontinue=0, param1=0, param2=0, param3=0,
                                                                       param4=0, x=0, y=0, z=0,
                                                                       mission_type=dialect.MAV_MISSION_TYPE_MISSION)
                    elif seq == 1:  # Takeoff
                        message = dialect.MAVLink_mission_item_message(target_system=self.target_system,
                                                                       target_component=self.target_component,
                                                                       seq=seq, frame=dialect.MAV_FRAME_GLOBAL,
                                                                       command=dialect.MAV_CMD_NAV_TAKEOFF, current=0,
                                                                       autocontinue=0, param1=0, param2=0, param3=0,
                                                                       param4=0, x=0, y=0, z=mission_list[0][2],
                                                                       mission_type=dialect.MAV_MISSION_TYPE_MISSION)
                    elif seq == len(mission_list) + 1:
                        message = dialect.MAVLink_mission_item_message(target_system=self.target_system,
                                                                       target_component=self.target_component,
                                                                       seq=seq, frame=dialect.MAV_FRAME_GLOBAL,
                                                                       command=dialect.MAV_CMD_NAV_LAND, current=0,
                                                                       autocontinue=0, param1=0, param2=0, param3=0,
                                                                       param4=0, x=mission_list[seq - 2][0],
                                                                       y=mission_list[seq - 2][1],
                                                                       z=mission_list[seq - 2][2],
                                                                       mission_type=dialect.MAV_MISSION_TYPE_MISSION)
                    else:
                        message = dialect.MAVLink_mission_item_message(target_system=self.target_system,
                                                                       target_component=self.target_component,
                                                                       seq=seq, frame=dialect.MAV_FRAME_GLOBAL,
                                                                       command=dialect.MAV_CMD_NAV_WAYPOINT, current=0,
                                                                       autocontinue=0, param1=0, param2=0, param3=0,
                                                                       param4=0, x=mission_list[seq - 2][0],
                                                                       y=mission_list[seq - 2][1],
                                                                       z=mission_list[seq - 2][2],
                                                                       mission_type=dialect.MAV_MISSION_TYPE_MISSION)
                    self.mav.mav.send(message)

            elif message["mavpackettype"] == "MISSION_ACK":
                if message["mission_type"] == dialect.MAV_MISSION_TYPE_MISSION and \
                        message["type"] == dialect.MAV_MISSION_ACCEPTED:
                    break

    def clear_Mission(self):
        message = dialect.MAVLink_mission_clear_all_message(target_system=self.target_system,
                                                            target_component=self.target_component,
                                                            mission_type=dialect.MAV_MISSION_TYPE_MISSION)
        self.mav.mav.send(message)

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

    def goto(self, lat, lon, alt, vx=0, vy=0, vz=0, afx=0, afy=0, afz=0, yaw=0, yaw_rate=0, mode=int(0b110111111000),
             coo_frame='GLOBAL'):
        if coo_frame == 'GLOBAL':
            FRAME = dialect.MAV_FRAME_GLOBAL_INT
        elif coo_frame == 'RELATIVE':
            FRAME = dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT
        elif coo_frame == 'TERRAIN':
            FRAME = dialect.MAV_FRAME_GLOBAL_TERRAIN_ALT_INT
        else:
            FRAME = dialect.MAV_FRAME_GLOBAL_INT
        message = dialect.MAVLink_set_position_target_global_int_message(time_boot_ms=10,
                                                                         target_system=self.target_system,
                                                                         target_component=self.target_component,
                                                                         coordinate_frame=FRAME, type_mask=mode,
                                                                         lat_int=lat*10**7, lon_int=lon*10**7, alt=alt,
                                                                         vx=vx, vy=vy, vz=vz, afx=afx, afy=afy, afz=afz,
                                                                         yaw=yaw, yaw_rate=yaw_rate)
        self.mav.mav.send(message)

    def getparam(self, ID):
        message = dialect.MAVLink_param_request_read_message(target_system=self.target_system,
                                                             target_component=self.target_component,
                                                             param_id=ID.encode("utf-8"), param_index=-1)
        self.mav.mav.send(message)

    def setparam(self, ID, value):
        message = dialect.MAVLink_param_set_message(target_system=self.target_system,
                                                    target_component=self.target_component, param_id=ID.encode("utf-8"),
                                                    param_value=value, param_type=dialect.MAV_PARAM_TYPE_REAL32)
        self.mav.mav.send(message)