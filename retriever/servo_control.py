#!/usr/bin/env python3
import time
import serial
import retriever as ret

cur_angle = 0
serialcomm = serial.Serial('/dev/cu.usbmodem101', 9600)



# cur_angle and angle are both 0 to 180
def rotate_servo(serialcomm, cur_angle, angle):
    print("going to rotate the servo 6 degrees at a time")
    print ("cur angle is " + str(cur_angle))
    print("angle that we're trying to rotate to is " + str(angle))
    time.sleep(1)

    incr = 1

    # attempt to rotate the servo 6 degrees at a time
    if cur_angle >= angle:
        incr = -1
        
    for temp_angle in range(cur_angle, angle , incr):
        print("temp angle is " + str(temp_angle))
        #t_angle_to_string = str(temp_angle) + "\n"
        #serialcomm.write(t_angle_to_string.strip().encode())
        serialcomm.write(chr(temp_angle).encode())
        time.sleep(0.1)
        #time.sleep(1)
    serialcomm.write(chr(angle).encode())
    time.sleep(0.1)

    return

#rotate_servo(180)

if __name__ == "__main__":
    print("we will be starting from an empty database")
    print("first we will rotate rack to 90 degrees")
    # rotate_servo(serialcomm, 0, 45)
    # time.sleep(0.3)
    # print("now we rotate from 90 to 360")
    # rotate_servo(serialcomm, 45, 180)
    # time.sleep(0.3)
    rotate_servo(serialcomm, 180, 0)