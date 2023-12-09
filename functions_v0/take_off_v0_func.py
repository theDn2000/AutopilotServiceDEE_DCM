import threading
import time


def take_off_trigger(self):
    print(self.state)
    w = threading.Thread(target=self.take_off_v0, args=[5, True])
    w.start()
    w.join()


def take_off_v0(self, a_target_altitude, manualControl):
    self.state = 'takingOff'
    self.vehicle.simple_takeoff(a_target_altitude)
    while True:
        print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if self.vehicle.location.global_relative_frame.alt >= a_target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

    self.state = 'flying'
