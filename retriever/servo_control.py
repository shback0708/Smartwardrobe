#!/usr/bin/env python3
# from pyfirmata import Arduino, util
import time
import serial
import retriever as ret

serialcomm = serial.Serial('/dev/cu.usbmodem101', 9600)
serialcomm.timeout = 1

while True:
    #angle = ret.getAngle()
    for i in range (0, 180, 20):
        #convert int to string
        angle = str(i) + "\n"
        serialcomm.write(angle.strip().encode())
        time.sleep(2)
    # if angle == "done":
    #     print("finished program")
    #     break
    # serialcomm.write(angle)
    
serialcomm.close()
