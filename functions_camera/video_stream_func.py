import base64
import cv2 as cv  # OpenCV
import threading
import time



def send_video_stream(self, callback): # Parecido a telemetry_info (hay que pasarle una función de callback)

    while self.sending_video_stream:
        # Read Frame
        ret, frame = self.cap.read()
        if ret:
            _, image_buffer = cv.imencode(".jpg", frame)
            jpg_as_text = base64.b64encode(image_buffer)
            callback(jpg_as_text)
            time.sleep(0.03333333333333333)  # 30 frames per second
            #print ("envio frame") # A MODIFICAR


def start_video_stream(self, callback):
    print("start video stream")
    self.sending_video_stream = True
    w = threading.Thread(target=self.send_video_stream, args=[callback])
    w.start()

def stop_video_stream(self):
    print("stop video stream")
    self.sending_video_stream = False
    