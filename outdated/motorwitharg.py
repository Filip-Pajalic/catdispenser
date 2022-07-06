from time import sleep
import RPi.GPIO as GPIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("revolution", help="display a square of a given number",
                    type=int)
args = parser.parse_args()

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
RELAY = 22 # Relay pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(RELAY, GPIO.OUT)
GPIO.output(DIR, CW)
GPIO.output(RELAY, GPIO.HIGH)
MODE = (14, 15, 18) # Microstep Resolution GPIO Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (1, 1, 1)}

GPIO.output(MODE, RESOLUTION['1/16'])

step_forward = 20
step_backward = 0
delay = 0.005
counter = 0

if args.revolution:
    print("Feeding for : % s revolutions." % args.revolution)
try:
    while counter < args.revolution:

        GPIO.output(DIR, CCW)
        for x in range(step_backward):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        GPIO.output(DIR, CW)
        for x in range(step_forward):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

        GPIO.output(DIR, CCW)
        counter = counter + 1
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()