#! /usr/bin/python2
from time import sleep
import time
import RPi.GPIO as GPIO
import sys
import argparse
import threading
import json
import serial
import glob

class Dispenser:
    
    DIR = 20   # Direction GPIO Pin
    STEP = 21  # Step GPIO Pin
    RELAY = 22 # Relay pin
    CW = 1     # Clockwise Rotation
    CCW = 0    # Counterclockwise Rotation
    SPR = 48   # Steps per rev (360 / 7.5)
    referenceUnit = 258

    
    def __init__(self, number):
        self.args=None
        self.number = number
        self.maxtime = 20
        self.totaltime = 0
        self.data = None
        self.grams = 0
        self.rel_path = "/home/pi/catfiles/catdata.json"
        self.ser=None
        self.serport=None
        self.baudrate="115200"
        
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
        self.findPortTeensy()
        self.ser = serial.Serial(port=self.serport,baudrate=self.baudrate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
        print "Connected to Teensy on: " + self.ser.portstr
        self.ser.close()
        self.startSerialTeensy()
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
        

    def findPortTeensy(self):
        dev  = "/dev/ttyACM*"
        scan = glob.glob(dev)
        if (len(scan) == 0):
            dev  = '/dev/ttyUSB*'
            scan = glob.glob(dev)
            if (len(scan) == 0):
                print "Unable to find any ports scanning for /dev/[ttyACM*|ttyUSB*]" + dev 
                sys.exit()  
        self.serport=scan[0]

    def startSerialTeensy(self):
        self.ser = serial.Serial(port=self.serport,baudrate=self.baudrate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
        acceptValues = b'a'
        self.ser.write(acceptValues)
        dummyValue = b'ok'
        self.ser.write(dummyValue)
        self.ser.close()
        self.ser = serial.Serial(port=self.serport,baudrate=self.baudrate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
        sleep(10)
        retries = 20
        while (retries > 0):
            try:
                line = self.ser.readline()
                if line:
                    print "Starting Teensy serial."
                    return True
            except KeyboardInterrupt:
                sys.exit()
            except:
                print "cant read value"
            pass
            sleep(0.1)
            print "Retry: " + str(21 - retries)
            retries = retries - 1
        return False
        self.ser.close()

    def stopTeensy(self):
        self.ser = serial.Serial(port=self.serport,baudrate=self.baudrate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
        print("Stopping Teensy connection.")
        stoppValue = b's'
        self.ser.write(stoppValue)
        dummyValue = b'ok'
        self.ser.write(dummyValue)
        retries = 20
        while (retries > 0):
            try:
                line = self.ser.readline()
                if line == "Stopped":
                    retires = 0
            except:
                print "cant read value"
            pass
            retries = retries - 1
        self.ser.close()

    def readLineTeensy(self):
        try:
            line = self.ser.readline()
            if line:
                return line
                #print (line),                               
        except:
            print "cant read value"
            pass
        return ""
        


    def cleanAndExit(self):      
        print("Final grams:")
        sleep(0.2)
        final = float(self.readLineTeensy())
        self.ser.close()
        deviation = self.grams - final 
        print(final)
        self.data['feed'+ self.number]['amountgiven'] = final        
        self.data['feed'+ self.number]['deviation'] = int(deviation)
        self.data['feed'+ self.number]['time'] = round(self.totaltime,1)
        with open(self.rel_path, 'w') as f:
            json.dump(self.data, f , indent=4)
        print("Cleaning...")
        GPIO.cleanup()
        self.stopTeensy()
        print("Bye!")
        sys.exit()



    def runMotor(self):
        step_forward = 19
        step_backward = 12
        delay = 0.00075
        weight = 0
        self.ser = serial.Serial(port=self.serport,baudrate=self.baudrate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
        program_starts = time.time()
        try:
            while weight < self.grams:
                weight = float(self.readLineTeensy())
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
          

def main(grams):    
    f = Dispenser(grams)    
    f.runMotor()
    f.cleanAndExit()

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    parser = argparse.ArgumentParser()
    parser.add_argument("grams", help="How much to feed in grams.",
                        type=str)
    args = parser.parse_args()
    main(args.grams)