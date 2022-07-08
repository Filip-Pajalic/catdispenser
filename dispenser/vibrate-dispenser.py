import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

pinForward = 26
pinReverse = 19

GPIO.setup(pinForward, GPIO.OUT)
GPIO.setup(pinReverse, GPIO.OUT)

p = GPIO.PWM(pinForward, 50)
q = GPIO.PWM(pinReverse, 50)
try:
    p.start(0)
    p.ChangeDutyCycle(40)
    sleep(2)
    p.stop()

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()