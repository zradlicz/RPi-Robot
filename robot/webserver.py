from flask import Flask, render_template, Response, request
from camera import DepthAIMonoCamera  # Assuming DepthAIMonoCamera is the camera class from your module
import stepper
import time

app = Flask(__name__)

camera = DepthAIMonoCamera()
print('Camera Initialized')
motor1 = stepper.Motor(step_pin=12, direction_pin=11, enable_pin=10)
motor2 = stepper.Motor(step_pin=15, direction_pin=16, enable_pin=17)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/start_motors", methods=["POST"])
def start_motors():
    motor1.start()
    motor2.start()
    return "Motors started"

@app.route("/stop_motors", methods=["POST"])
def stop_motors():
    motor1.stop()
    motor2.stop()
    return "Motors stopped"

@app.route("/update_pwm", methods=["POST"])
def update_pwm():
    data = request.get_json()
    motor_id = data.get("motorId")
    pwm_value = data.get("pwmValue")
    if motor_id == "motor1":
        motor1.set_value(int(pwm_value)/100)
    elif motor_id == "motor2":
        motor2.set_value(int(pwm_value)/100)
    return "PWM updated"

def gen_frames():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
