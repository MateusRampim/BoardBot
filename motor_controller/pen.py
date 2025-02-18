from RpiMotorLib import rpi_pservo_lib

class Pen:
    def __init__(self, pin, lifted, pressed):
        self.pos_lifted = lifted
        self.pos_pressed = pressed

        self.pin = pin
        self.servo = rpi_pservo_lib.ServoPigpio("Sone", 50, 1000, 2000)

    def lift(self):
        self.servo.servo_move_step(
            servo_pin=self.pin,
            start=self.pos_pressed,
            end=self.pos_lifted,
            stepdelay=0.01,
            stepsize=1,
            verbose=True
        )

    def press(self):
        self.servo.servo_move_step(
            servo_pin=self.pin,
            start=self.pos_lifted,
            end=self.pos_pressed,
            stepdelay=0.01,
            stepsize=1,
            verbose=True
        )

