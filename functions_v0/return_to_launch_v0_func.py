import threading
import dronekit
import time


def returning_trigger(self):
    self.vehicle.mode = dronekit.VehicleMode("RTL")
    self.state = 'returningHome'
    self.direction = "RTL"
    self.going = True
    w = threading.Thread(target=self.returning_v0)
    w.start()


def returning_v0(self):
    # wait until the drone is at home
    while self.vehicle.armed:
        time.sleep(1)
    self.state = 'onHearth'
