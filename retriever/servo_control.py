#!/usr/bin/env python3
# from pyfirmata import Arduino, util
from time import sleep
import serial
# This function will be imported from retriever.py
from retriever import 
# def servo_control():
#     board = Arduino('COM4')
#     pin_9 = board.get_pin('d:9:p') # pwm pin
#     print ("sending out pwm signal")

#     angle = 0
#     while True:
#         update_angle(angle)
#         pin_9.write(angle)
#         sleep(2)

#     return

# arduino_data = serial.Serial('/dev/cu.usbmodem1101', 9600)
# arduino_data.timeout = 1

# while 1:
#     i = input("input open or close: ").strip()
#     if i == "done":
#         print ("finished program")
#         break
    
#     arduino_data.write(i.encode())
#     time.sleep(0.5)
#     print(arduino_data.readline().decode('ascii'))

# arduino_data.close()

# This might be completely unnecessary

# Once the arduino script of retriever api is loaded into the board,
# we are able to just call this function

# So here currently I have tested that we can take an input 

import serial
import time

serialcomm = serial.Serial('/dev/cu.usbmodem1101', 9600)
serialcomm.timeout = 1

while True:
    #i = input("input(open/close): ").strip()
    #if i == "done":
    #    print ("finished program")
    #    break
    #serialcomm.write(i.encode())

    angle = getAngle()
    serialcomm.write(angle)
    
serialcomm.close()
