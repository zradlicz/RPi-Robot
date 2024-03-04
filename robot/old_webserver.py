from flask import Flask, render_template, Response
import cv2
import depthai as dai
import argparse

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


    

def gen_frames():
    
     # Create pipeline
    pipeline = dai.Pipeline()

    # Define sources and outputs
    camMono = pipeline.create(dai.node.MonoCamera)
    xoutMono = pipeline.create(dai.node.XLinkOut)

    xoutMono.setStreamName("mono")

    # Linking
    camMono.out.link(xoutMono.input)

    # Connect to device and start pipeline
    with dai.Device(pipeline) as device:

        # Clear queue events
        device.getQueueEvents()

        while True:
            # Block until a message arrives to any of the specified queues
            queueName = device.getQueueEvent(("mono"))

            # Getting that message from queue with name specified by the event
            # Note: number of events doesn't necessarily match number of messages in queues
            # because queues can be set to non-blocking (overwriting) behavior
            message = device.getOutputQueue(queueName).get()
            frameRgb = message.getCvFrame()
            ret, buffer = cv2.imencode('.jpg', frameRgb)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



        


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")