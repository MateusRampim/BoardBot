from RpiMotorLib import rpiservolib

class Pen:
    def __init__(self, pin, lifted, pressed):
        self.pos_lifted = lifted
        self.pos_pressed = pressed

        self.pin = pin
        self.servo = rpiservolib.SG90servo()

    def lift(self):
        self.servo.servo_move(servo_pin=self.pin, position=self.pos_lifted, delay=0.5, verbose=True)

    def press(self):
        self.servo.servo_move(servo_pin=self.pin, position=self.pos_pressed, delay=0.5, verbose=True)
