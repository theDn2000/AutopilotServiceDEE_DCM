import base64
import cv2 as cv  # OpenCV

def take_picture(self):
    print("Take picture")
    ret = False
    for n in range(1, 20):
        # this loop is required to discard first frames
        ret, frame = self.cap.read()
        _, image_buffer = cv.imencode(".jpg", frame)
        # Converting into encoded bytes
        jpg_as_text = base64.b64encode(image_buffer)


        return jpg_as_text