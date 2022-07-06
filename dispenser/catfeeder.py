#! /usr/bin/python2
from time import sleep
import time
import RPi.GPIO as GPIO
from hx711 import HX711
import sys
import argparse
import threading
import json


class Feeder:
    
    DIR = 20   # Direction GPIO Pin
    STEP = 21  # Step GPIO Pin
    RELAY = 22 # Relay pin
    CW = 1     # Clockwise Rotation
    CCW = 0    # Counterclockwise Rotation
    SPR = 48   # Steps per rev (360 / 7.5)
    referenceUnit = 258

    
    def __init__(self, number):
        self.hx = HX711(23, 16)
        self.args=None
        self.number = number
        self.maxtime = 20
        self.totaltime = 0
        self.data = None
        self.grams = 0
        self.rel_path = "/home/pi/catfiles/catdata.json"
        
        with open(self.rel_path) as json_file:
            self.data = json.load(json_file)
        
        if self.number == "1":
            self.grams = self.data['feed'+ self.number]['wanted']
        if self.number == "2":
            self.grams = self.data['feed'+ self.number]['wanted'] - self.data['feed1']['deviation']
        if self.number == "3":
            self.grams = self.data['feed'+ self.number]['wanted'] - self.data['feed2']['deviation']
        print(self.grams)
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



    def cleanAndExit(self):      
        print("Final grams:")
        sleep(0.2)
        final = self.hx.get_weight(19)
        deviation = self.grams - final 
        print(final)
        
        self.data['feed'+ self.number]['amountgiven'] = final        
        self.data['feed'+ self.number]['deviation'] = int(deviation)
        self.data['feed'+ self.number]['time'] = round(self.totaltime,1)
        with open(self.rel_path, 'w') as f:
            json.dump(self.data, f , indent=4)
        self.hx.power_down()
        print("Cleaning...")
        GPIO.cleanup()
        print("Bye!")
        sys.exit()



    def runMotor(self):
        step_forward = 19
        step_backward = 12
        delay = 0.00075
        weight = 0
        program_starts = time.time()
        try:
            while weight < self.grams-1:
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
                if (self.totaltime) > 30:
                    weight = self.grams
        except KeyboardInterrupt:
            return      
          

def main(number):    
    f = Feeder(number)    
    f.runMotor()
    f.cleanAndExit()

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="what time of day to feed",
                        type=str)
    args = parser.parse_args()

    main(args.number)