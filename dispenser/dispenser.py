#! /usr/bin/python2
from time import sleep
import time
import RPi.GPIO as GPIO
from hx711 import HX711
import sys
import argparse
import json
from datetime import date


class Dispenser:

    DIR = 20   # Direction GPIO Pin
    STEP = 21  # Step GPIO Pin
    RELAY = 22 # Relay pin
    CW = 1     # Clockwise Rotation
    CCW = 0    # Counterclockwise Rotation
    SPR = 48   # Steps per rev (360 / 7.5)
    referenceUnit = 258


    def __init__(self, preset, amount):
        self.hx = HX711(23, 16)
        self.preset = preset
        self.amount = amount
        self.maxtime = 20
        self.totaltime = 0
        self.data = None
        self.grams = 0
        self.rel_path = "/home/pi/config/config.json"
        self.skip = False
        self.error = ""

        today = date.today()
        d1 = today.strftime("%y%m%d")
        
        print("#######################################################")
        print("Date: " + d1)
        

        
        with open(self.rel_path) as json_file:
            self.data = json.load(json_file)

        if self.preset == "morning":
            if self.data['feed1']['skip'] == "true":
                self.skip = True
            self.grams = self.data['feed1']['wanted']
        if self.preset == "dinner":
            if self.data['feed2']['skip'] == "true":
                self.skip = True
            self.grams = self.data['feed2']['wanted']
        if self.preset == "night":
            if self.data['feed3']['skip'] == "true":
                self.skip = True
            self.grams = self.data['feed3']['wanted']
        if self.preset == "other":
            print("Feeding non scheduled meal.")
            self.grams = self.amount
        print("Feeding for amount: " + str(self.grams))
        if self.skip == False:
            self.init()

    def init(self):
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.RELAY, GPIO.OUT)
        GPIO.output(self.DIR, self.CW)
        GPIO.output(self.RELAY, GPIO.HIGH)
        MODE = (14, 15, 18) # Microstep Resolution GPIO Pins
        GPIO.setup(MODE, GPIO.OUT)
        RESOLUTION = {'Full': (0, 0, 0),
                'Half': (1, 0, 0),
                '1/4': (0, 1, 0),
                '1/8': (1, 1, 0),
                '1/16': (1, 1, 1)}

        GPIO.output(MODE, RESOLUTION['1/16'])
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(self.referenceUnit)
        self.hx.reset()
        self.hx.tare()
        self.hx.power_up()
        print("Tare done!")

    def runMotor(self):
        step_forward = 35
        step_backward = 20
        delay = 0.00075
        weight = 0
        program_starts = time.time()
        try:
            while weight < self.grams-3:
                weight = self.hx.get_weight(5)
                print("Current grams:")
                print(weight)
                GPIO.output(self.DIR, self.CCW)
                for x in range(step_backward):
                    GPIO.output(self.STEP, GPIO.HIGH)
                    sleep(delay)
                    GPIO.output(self.STEP, GPIO.LOW)
                    sleep(delay)
                GPIO.output(self.DIR, self.CW)
                for x in range(step_forward):
                    GPIO.output(self.STEP, GPIO.HIGH)
                    sleep(delay)
                    GPIO.output(self.STEP, GPIO.LOW)
                    sleep(delay)
                now = time.time()
                self.totaltime = now - program_starts
                if (self.totaltime) > 15:
                    weight = self.grams
                    self.error = "Exceeded time"
        except KeyboardInterrupt:
            return

    def cleanAndExit(self):
        print("Final grams:")
        sleep(0.2)
        final = self.hx.get_weight(19)
        deviation = self.grams - final
        if(deviation > -8):
            self.error = "Weight issue"
        if(deviation < 8):
            self.error = "Weight issue"
        print(final)
        number = "1"
        if self.preset == "dinner":
            number = "2"
        if self.preset == "night":
            number = "3"
        if not (self.preset == "other"):
            self.data['feed'+ number]['amountgiven'] = final
            self.data['feed'+ number]['deviation'] = int(deviation)
            self.data['feed'+ number]['time'] = round(self.totaltime,1)
            if self.error != "":
                self.data['feed'+ number]['error'] = "error"
                self.data['feed'+ number]['error-reason'] = self.error
        else:
            self.data['other']['amountgiven'] = final
            self.data['other']['deviation'] = int(deviation)
            self.data['other']['time'] = round(self.totaltime,1)
            if self.error != "":
                self.data['other']['error'] = "error"
                self.data['other']['error-reason'] = self.error
        with open(self.rel_path, 'w') as f:
            json.dump(self.data, f , indent=4)
        self.hx.power_down()
        print("Cleaning...")
        GPIO.cleanup()
        print("Bye!")
        sys.exit()

def main(preset, amount):
    d = Dispenser(preset, amount)
    if d.skip == False:
        d.runMotor()
        d.cleanAndExit()
    print("Meal skipped")

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    parser = argparse.ArgumentParser()
    parser.add_argument("preset", help="What preset to use, morning, dinner, night, other.",
                        type=str)
    parser.add_argument("amount", help="How much if preset is other",
                        type=int)
    args = parser.parse_args()
    main(args.preset, args.amount)