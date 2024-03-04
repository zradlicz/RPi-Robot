import gpiozero as GPIO
import time

class Motor:
    def __init__(self, step_pin, direction_pin, enable_pin):
        self.state = "stopped"
        self.direction = "cw"
        
        self.pwm = GPIO.PWMOutputDevice(step_pin)
        self.pwm.frequency = 1000
        self.pwm.value = .5

        self.direction = GPIO.OutputDevice(direction_pin)
        self.direction.off()

        self.enable = GPIO.OutputDevice(enable_pin)
        self.enable.on()

    def start(self):
        if self.state == "stopped":
            self.enable.off()
            self.pwm.on()
            self.state = "running"
            print("Motor started")
        else:
            print("Motor is already running")

    def stop(self):
        if self.state == "running":
            self.enable.on()
            self.pwm.off()
            self.state = "stopped"
            print("Motor stopped")
        else:
            print("Motor is already stopped")

    def set_pwm_frequency(self, frequency):
        self.pwm.frequency = frequency
        print(f"PWM frequency set to {frequency} Hz")

    def set_value(self, value):
        self.pwm.value = value
        print(f"Duty cycle set to {value}%")