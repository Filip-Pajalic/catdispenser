import RPi.GPIO as GPIO

RELAY = 22 # Relay pin

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(RELAY, GPIO.OUT)
GPIO.output(RELAY, GPIO.LOW)

GPIO.cleanup()