#!/bin/env python
#
# From: earl@microcontrollerelectonics.com
#
 
import serial
import sys
import glob
import time

def findPort():
  dev  = "/dev/ttyACM*"
  scan = glob.glob(dev)
  if (len(scan) == 0):
    dev  = '/dev/ttyUSB*'
    scan = glob.glob(dev)
    if (len(scan) == 0):
      print "Unable to find any ports scanning for /dev/[ttyACM*|ttyUSB*]" + dev 
      sys.exit()  
  return scan[0]
  


def startConnection():
  ser = serial.Serial(port=serport,baudrate=rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
  acceptValues = b'a'
  ser.write(acceptValues)
  dummyValue = b'ok'
  ser.write(dummyValue)
  ser.close()
  ser = serial.Serial(port=serport,baudrate=rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
  time.sleep(10)
  retries = 20
  while (retries > 0):
    try:
      line = ser.readline()
      if line:
        print "Starting Teensy serial."
        return True
    except KeyboardInterrupt:
      sys.exit()
    except:
      print "cant read value"
      pass
    time.sleep(0.1)
    print "Retry: " + str(21 - retries)
    retries = retries - 1
  return False
  ser.close()

def readLineTeensy():
  ser = serial.Serial(port=serport,baudrate=rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
  try:
    line = ser.readline()
    if line:
      print (line),
  except:
    print "cant read value"
    pass
  ser.close()


def stopTeensy():
  ser = serial.Serial(port=serport,baudrate=rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
  print("Stopping Teensy connection.")
  stoppValue = b's'
  ser.write(stoppValue)
  dummyValue = b'ok'
  ser.write(dummyValue)
  retries = 20
  while (retries > 0):
    try:
        line = ser.readline()
        if line == "Stopped":
          retires = 0
    except:
      print "cant read value"
      pass
    retries = retries - 1
  ser.close()

rate = "115200"
#MAIN
serport = findPort()
ser = serial.Serial(port=serport,baudrate=rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=.1)
print "Connected to Teensy on: " + ser.portstr
ser.close()

if startConnection():
  i = 0
  while i < 30:
    time.sleep(0.1)
    readLineTeensy()
    i = i + 1
  stopTeensy()  
 
ser.close()
sys.exit()