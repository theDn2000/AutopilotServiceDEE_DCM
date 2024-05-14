import ssl

import cv2 as cv # OpenCV 
from Camera import Camera
import paho.mqtt.client as mqtt
import base64
import threading
import time
import websockets
import asyncio

import json


def process_message(message,   client):

    global sending_video_stream
    global sending_video_for_calibration
    global finding_colors
    global origin
    global cap

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    camera_id = splited[3]
    print("recibo ", command, "de ", origin)

    if command == "takePicture":
        # Check if the camera is the requested one
        if service_id == camera_id:
            # Take a picture
            jpg_as_text = camera.take_picture()
            # Publish the image to the broker
            client.publish("CameraService/" + origin + "/picture/" + str(camera_id), jpg_as_text)

    if command == "startVideoStream":
        # Check if the camera is the requested one
        if service_id == camera_id:
            # Start the video stream
            camera.start_video_stream(callback_broker)

    if command == "stopVideoStream":
        # Check if the camera is the requested one
        if service_id == camera_id:
            # Stop the video stream
            camera.stop_video_stream()




def callback_broker(jpg_as_text):
    # Publish the image to the broker (for video streaming)
    external_client.publish("CameraService/" + origin + "/picture/" + str(service_id), jpg_as_text)

def on_internal_message(client, userdata, message):
    print("recibo internal ", message.topic)
    global internal_client
    process_message(message, internal_client)


def on_external_message(client, userdata, message):
    print("recibo external ", message.topic)

    global external_client
    process_message(message, external_client)


def on_connect(external_client, userdata, flags, rc):
    if rc == 0:
        print("Connection OK")
    else:
        print("Bad connection")


def CameraService(connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client
    global state
    global cap
    global colorDetector

    sending_video_stream = False

    cap = cv.VideoCapture(0)  # video capture source camera (Here webcam of lap>

    print("Camera ready")

    print("Connection mode: ", connection_mode)
    print("Operation mode: ", operation_mode)
    op_mode = operation_mode

    state = "disconnected"

    print("Connection mode: ", connection_mode)
    print("Operation mode: ", operation_mode)
    op_mode = operation_mode



    if connection_mode == "global":
        if external_broker == "hivemq":
            external_client.connect("broker.hivemq.com", 8000)
            print("Connected to broker.hivemq.com:8000")

        elif external_broker == "hivemq_cert":
            external_client.tls_set(
                ca_certs=None,
                certfile=None,
                keyfile=None,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS,
                ciphers=None,
            )
            external_client.connect("broker.hivemq.com", 8884)
            print("Connected to broker.hivemq.com:8884")

        elif external_broker == "classpip_cred":
            external_client.username_pw_set(username, password)
            external_client.connect("classpip.upc.edu", 8000)
            print("Connected to classpip.upc.edu:8000")

        elif external_broker == "classpip_cert":
            external_client.username_pw_set(username, password)
            external_client.tls_set(
                ca_certs=None,
                certfile=None,
                keyfile=None,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS,
                ciphers=None,
            )
            external_client.connect("classpip.upc.edu", 8883)
            print("Connected to classpip.upc.edu:8883")
        elif external_broker == "localhost":
            external_client.connect("localhost", 8000)
            print("Connected to localhost:8000")
        elif external_broker == "localhost_cert":
            print("Not implemented yet")

    elif connection_mode == "local":
        if operation_mode == "simulation":
            external_client.connect("localhost", 8000)
            print("Connected to localhost:8000")
        else:
            external_client.connect("10.10.10.1", 8000)
            print("Connected to 10.10.10.1:8000")

    print("Waiting....")
    external_client.subscribe("+/CameraService/#", 2)
    internal_client.subscribe("+/CameraService/#")
    internal_client.loop_start()
    external_client.loop_forever()


def process_output_video_stream(origin, data): # Callback function that publishes data to the broker
    
    topic_to_publish = f"CameraService/{origin}/videoFrame"
    external_client.publish(topic_to_publish, data)
    time.sleep(0.2)


# WEB SOCKETS
async def send_video_stream(websocket, path):
    queue = asyncio.Queue()
    # Callback function that sends the video stream to the client
    
    async def send_jpg_as_text(jpg_as_text):
        # Send the frame to the client through the websocket
        print ("envio frame: "+ str(len(jpg_as_text)) + " bytes")
        await websocket.send(jpg_as_text)
    
    def callback_websocket(jpg_as_text):
        queue.put_nowait(jpg_as_text)
        # asyncio.run_coroutine_threadsafe(send_jpg_as_text(jpg_as_text), loop)
    
    # Function that recieves the client message and processes it to start or stop sending video stream
    print("Starting video stream via Websocket")
    async for message in websocket:
        # Split the message
        splited = message.split("/")
        origin = splited[0]
        command = splited[2]
        camera_id = splited[3]

        # Check if the ID of the camera is the same as the requested one
        if service_id == camera_id:
            if command == "startVideoStream":
                # Start the video stream
                #jpg_as_text = camera.take_picture()
                camera.start_video_stream(callback_websocket)
                # Once the video stream is started, send the frames to the client
                while sending_video_stream == True:
                    jpg_as_text = await queue.get()
                    if jpg_as_text is None:
                        print("No more frames")
                        break
                    await websocket.send(jpg_as_text)
                    #await websocket.send(jpg_as_text)
                #await websocket.send(jpg_as_text)
                
            elif command == "stopVideoStream":
                # Stop the video stream
                camera.stop_video_stream()


async def start_websocket_server():
    # Start the websocket server
    port = 8765
    print("- CameraService: Websocket server listening on port:", port)
    websocket = websockets.serve(send_video_stream, "localhost", port)
    await websocket


def start_websocket_server_in_thread():
    # Function to call when starting the thread
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.get_event_loop().run_until_complete(start_websocket_server())
    asyncio.get_event_loop().run_forever()



import cv2 as cv

if __name__ == "__main__":
    import sys

    # Inicialize variables
    service_id = sys.argv[1]
    connection_mode = sys.argv[2]  # global or local
    operation_mode = sys.argv[3]  # simulation or production
    username = None
    password = None

    if connection_mode == "global":
        external_broker = sys.argv[4]
        if external_broker == "classpip_cred" or external_broker == "classpip_cert":
            username = sys.argv[5]
            password = sys.argv[6]
    else:
        external_broker = None

    internal_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Autopilot_internal")
    internal_client.on_message = on_internal_message
    internal_client.connect("localhost", 1884)
    
    internal_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Camera_internal")
    internal_client.on_message = on_internal_message
    internal_client.connect("localhost", 1884)

    external_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Camera_external", transport="websockets")
    external_client.on_message = on_external_message
    external_client.on_connect = on_connect

    # Create object Camera
    ID = 1 # A MODIFICAR
    camera = Camera(ID)

    # WebSockets parameters
    loop = asyncio.new_event_loop()

    # Thread to inicialize web socket
    wst = threading.Thread(target=start_websocket_server_in_thread)
    wst.start()

    CameraService(connection_mode, operation_mode, external_broker, username, password)
