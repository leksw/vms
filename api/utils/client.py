import zmq
import sys
import numpy
import cv2

import asyncio


HOST = "zmq"
PORT = "4444"


class Client:
    """Using zmq data as stream"""

    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self._context = zmq.Context()
        self._subscriber = self._context.socket(zmq.SUB)

    def decode_array(self, array):
        return cv2.imencode(".jpg", array)[1].tobytes()

    async def recv_array(self, flags=0, copy=True, track=False):
        """recv a numpy array"""
        self._subscriber.connect("tcp://{}:{}".format(self.host, self.port))
        self._subscriber.setsockopt(zmq.SUBSCRIBE, b"")
        while True:
            md = self._subscriber.recv_json(flags=flags)
            msg = self._subscriber.recv(flags=flags, copy=copy, track=track)
            buf = memoryview(msg)
            A = numpy.frombuffer(buf, dtype=md["dtype"])
            yield self.decode_array(A.reshape(md["shape"]))
            await asyncio.sleep(1 / 120)
