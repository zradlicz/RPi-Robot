import depthai as dai
import cv2
import time

class DepthAIMonoCamera:
    def __init__(self):
        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Define sources and outputs
        self.camMono = self.pipeline.create(dai.node.MonoCamera)
        self.xoutMono = self.pipeline.create(dai.node.XLinkOut)

        self.xoutMono.setStreamName("mono")

        # Linking
        self.camMono.out.link(self.xoutMono.input)

        # Connect to device and start pipeline
        self.device = dai.Device(self.pipeline)

        # Clear queue events
        self.device.getQueueEvents()

    def get_frame(self):
        start_time = time.time()

        queueName = self.device.getQueueEvent(("mono"))
        queue_time = time.time() - start_time

        start_time = time.time()
        message = self.device.getOutputQueue(queueName).get()
        message_time = time.time() - start_time

        start_time = time.time()
        frameRgb = message.getCvFrame()
        frameRgb = cv2.resize(frameRgb, None, fx=.1, fy=.1)
        frame_rgb_time = time.time() - start_time

        start_time = time.time()
        ret, buffer = cv2.imencode('.jpg', frameRgb)
        encode_time = time.time() - start_time

        frame = buffer.tobytes()

        if queue_time > .1: print("Queue time:", queue_time)
        if message_time > .1: print("Message retrieval time:", message_time)
        if frame_rgb_time > .1: print("Frame extraction time:", frame_rgb_time)
        if encode_time > .1: print("Encoding time:", encode_time)

        return frame
