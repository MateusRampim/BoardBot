import RPi.GPIO as GPIO

from RpiMotorLib import RpiMotorLib
    
GPIO_pins = (-1, -1, -1)
step0 = 15
dir0 = 16
step1 = 18
dir1 = 22

motor0 = RpiMotorLib.A4988Nema(dir0, step0, GPIO_pins, "DRV8825")
motor1 = RpiMotorLib.A4988Nema(dir1, step1, GPIO_pins, "DRV8825")


motor0.motor_go(False, "Full" , 30, .01, True, .05)
motor1.motor_go(False, "Full" , 30, .01, True, .05)

motor0.motor_go(True, "Full" , 30, .01, True, .05)
motor1.motor_go(True, "Full" , 30, .01, True, .05)
