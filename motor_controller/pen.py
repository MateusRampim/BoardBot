from RpiMotorLib import rpi_pservo_lib

class Pen:
    def __init__(self, pin, lifted, pressed):
        self.pos_lifted = lifted
        self.pos_pressed = pressed

        self.pin = pin
        self.servo = rpi_pservo_lib.ServoPigpio("Sone", 50, 1000, 2000)

    def lift(self):
        self.servo.servo_move(servo_pin=self.pin, position=self.pos_lifted, delay=0.5, verbose=False)

    def press(self):
        self.servo.servo_move(servo_pin=self.pin, position=self.pos_pressed, delay=0.5, verbose=False)
