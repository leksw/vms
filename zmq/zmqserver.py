import zmq
import cv2
import numpy as np

HOST = "0.0.0.0"
PORT = "4444"


class SocketNumpyServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://{}:{}".format(self.host, self.port))

    def send_array(self, A, flags=0, copy=True, track=False):
        """Send a numpy array with metadata"""
        md = dict(dtype=str(A.dtype), shape=A.shape,)
        self.socket.send_json(md, flags | zmq.SNDMORE)
        return self.socket.send(A, flags, copy=copy, track=track)


class Camera:
    def __init__(self):
        self.video_source = 0

    def frames(self):
        camera = cv2.VideoCapture(self.video_source)
        if not camera.isOpened():
            raise RuntimeError("Could not start camera.")

        frameWidth = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while True:
            ret, img = camera.read()
            if not ret:
                break

            yield np.array(img)

        camera.release()


if __name__ == "__main__":
    server = SocketNumpyServer()
    stream = Camera()
    for f in stream.frames():
        server.send_array(f)
