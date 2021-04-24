#!/usr/bin/env python3
import time
import serial
import retriever as ret

# cur_angle and angle are both 0 to 180
def rotate_servo(cur_angle, angle):
    print("going to rotate the servo 6 degrees at a time")
    print(angle)
    time.sleep(1)

    # attempt to rotate the servo 6 degrees at a time
    if cur_angle >= angle:
        for temp_angle in range(cur_angle, angle , -3):
            t_angle_to_string = str(temp_angle) + "\n"
            serialcomm.write(angle_to_string.strip().encode())
            time.sleep(0.2)
        angle_to_string = str(angle) + "\n"
        serialcomm.write(angle_to_string.strip().encode())
        time.sleep(1)
    else:
        # angle > cur_angle so increment
        for temp_angle in range(cur_angle, angle , 3):
            t_angle_to_string = str(temp_angle) + "\n"
            serialcomm.write(angle_to_string.strip().encode())
            time.sleep(0.2)
        angle_to_string = str(angle) + "\n"
        serialcomm.write(angle_to_string.strip().encode())
        time.sleep(1)
    return

#rotate_servo(180)