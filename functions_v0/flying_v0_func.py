import threading
import time
from pymavlink import mavutil


def flying_trigger(self):
    w = threading.Thread(target=self.flying_v0)
    w.start()


def flying_v0(self):
    speed = 1
    end = False
    cmd = self.prepare_command(0, 0, 0)  # stop
    while not end:
        self.going = False
        while not self.going:
            if not self.reaching_waypoint:
                self.vehicle.mav.send(cmd)
                time.sleep(1)
        # a new go command has been received. Check direction
        # print('salgo del bucle por ', self.direction)
        if self.direction == "North":
            cmd = self.prepare_command(speed, 0, 0)  # NORTH
        if self.direction == "South":
            cmd = self.prepare_command(-speed, 0, 0)  # SOUTH
        if self.direction == "East":
            cmd = self.prepare_command(0, speed, 0)  # EAST
        if self.direction == "West":
            cmd = self.prepare_command(0, -speed, 0)  # WEST
        if self.direction == "NorthWest":
            cmd = self.prepare_command(speed, -speed, 0)  # NORTHWEST
        if self.direction == "NorthEast":
            cmd = self.prepare_command(speed, speed, 0)  # NORTHEST
        if self.direction == "SouthWest":
            cmd = self.prepare_command(-speed, -speed, 0)  # SOUTHWEST
        if self.direction == "SouthEast":
            cmd = self.prepare_command(-speed, speed, 0)  # SOUTHEST
        if self.direction == "Stop":
            cmd = self.prepare_command(0, 0, 0)  # STOP
        if self.direction == "RTL":
            end = True


def prepare_command(self, velocity_x, velocity_y, velocity_z):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = mavutil.mavlink.MAVLink_set_position_target_global_int_message(
        0,  # time_boot_ms (not used)
        self.vehicle.target_system,
        self.vehicle.target_component,  # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0,
        0,
        0,  # x, y, z positions (not used)
        velocity_x,
        velocity_y,
        velocity_z,  # x, y, z velocity in m/s
        0,
        0,
        0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0,
        0,
    )  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    return msg


def go_order(self, direction):
    self.direction = direction
    print("- Autopilot Service: Going ", self.direction)
    self.going = True
