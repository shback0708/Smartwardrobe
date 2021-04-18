#!/usr/bin/env python3
import time
import serial
import retriever as ret

def rotate_servo(angle):
    print("is it going in")
    print(angle)
    serialcomm = serial.Serial('/dev/cu.usbmodem1101', 9600)
    #serialcomm.timeout = 1
    time.sleep(1)
    angle_to_string = str(angle) + "\n"
    serialcomm.write(angle_to_string.strip().encode())
    time.sleep(2)
    serialcomm.close()
    return

#rotate_servo(180)

# we don't need a while true loop
# if we just want to test the servo we just uncomment the part below
# and comment the part above

# serialcomm = serial.Serial('/dev/cu.usbmodem101', 9600)
# serialcomm.timeout = 1
# while True:
#     #angle = ret.getAngle()
#     for i in range (0, 180, 20):
#         #convert int to string
#         angle = str(i) + "\n"
#         serialcomm.write(angle.strip().encode())
#         time.sleep(2)
#     # if angle == "done":
#     #     print("finished program")
#     #     break
#     # serialcomm.write(angle)
    
# serialcomm.close()
