#! /usr/bin/python

from time import sleep
from src.TMC_2209.TMC_2209_StepperDriver import *
import time

import RPi.GPIO as GPIO
from HX711 import *


import sys
import argparse
import json
from datetime import date


class Dispenser:

    referenceUnit = -3068
    servoPIN = 13
    pwm = None    


    def __init__(self, preset, amount):
        self.hx = SimpleHX711(5, 6, -370, -367471)
        self.tmc = tmc = TMC_2209(23, 16, 20)
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
            print("Scheduled Feed 05:00")
            if self.data['feed1']['skip'] == "true":                
                self.skip = True
            self.grams = self.data['feed1']['wanted']
        if self.preset == "dinner":
            print("Scheduled Feed 18:00")
            if self.data['feed2']['skip'] == "true":                
                self.skip = True
            self.grams = self.data['feed2']['wanted']
        if self.preset == "night":
            print("Scheduled Feed 22:00")
            if self.data['feed3']['skip'] == "true":                
                self.skip = True
            self.grams = self.data['feed3']['wanted']
        if self.preset == "other":
            print("Feeding non scheduled meal.")
            self.grams = self.amount
            self.data['other']['wanted'] = int(self.amount)
        print("Feeding for amount: " + str(self.grams))
        if self.skip == False:
            self.init()

    def init(self):
        GPIO.setup(self.servoPIN, GPIO.OUT)
        self.pwm=GPIO.PWM(self.servoPIN, 50)
        self.pwm.start(0)
        self.SetAngle(34.3)
        self.hx.setUnit(Mass.Unit.G)
        self.hx.zero()
        
        print("Tare done!")
        self.tmc.set_loglevel(Loglevel.DEBUG)
        self.tmc.set_movement_abs_rel(MovementAbsRel.ABSOLUTE)
        self.tmc.set_direction_reg(False)
        self.tmc.set_current(300)
        self.tmc.set_interpolation(True)
        self.tmc.set_spreadcycle(False)
        self.tmc.set_microstepping_resolution(16)
        self.tmc.set_internal_rsense(False)
        self.tmc.readIOIN()
        self.tmc.readCHOPCONF()
        self.tmc.readDRVSTATUS()
        self.tmc.readGCONF()
        self.tmc.set_acceleration(4000)
        self.tmc.set_max_speed(500)
        self.tmc.set_motor_enabled(True)


    def SetAngle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(self.servoPIN, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(self.servoPIN, False)
        self.pwm.ChangeDutyCycle(0)


    

    def runMotor(self):
        step_forward = 35
        step_backward = -20
       
        weight = 0
        program_starts = time.time()
        try:
            while weight < self.grams-3:
                weight = self.hx.read(Options(int(3)))
                print("Current grams:")
                print(weight)
                self.tmc.run_to_position_steps(step_forward, MovementAbsRel.RELATIVE)
                self.tmc.run_to_position_steps(step_backward, MovementAbsRel.RELATIVE) 
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
        final = self.hx.read(Options(int(3)))
        deviation = self.grams - final
        if deviation < -5 or deviation > 5:
            self.error = "Weight issue"
        print(final)
        self.SetAngle(130)
        self.pwm.stop()
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
        if self.preset == "other":
            self.data['other']['amountgiven'] = final
            self.data['other']['deviation'] = int(deviation)
            self.data['other']['time'] = round(self.totaltime,1)
            if self.error != "":
                self.data['other']['error'] = "error"
                self.data['other']['error-reason'] = self.error
        with open(self.rel_path, 'w') as f:
            json.dump(self.data, f , indent=4)
        self.tmc.set_motor_enabled(False)
        self.tmc.deinit()
        del self.tmc
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