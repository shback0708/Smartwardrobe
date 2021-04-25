# This is be the demo file which we will use for the demo tomorrow
import database.database as db
import retriever.servo_control as sc
import time
import serial

def add(database, color):
    # add to database
    i = db.find_index_to_add(database)
    db.add_to_database(database, i, "tshirt", color)
    # after we add to database, we will rotate the servo
    sc.rotate_servo(i * 9)
    time.sleep(1)
    
    return 0

def ret(database, color):
    # add back to the database
    return 0

def take(database, color):
    # remove from database 
    i = db.find_clothes_index(database, "tshirt", color)
    db.remove_from_database(database, i)
    if i != -1:
        sc.rotate_servo(i * 9)
    else:
        print ("given clothes spec doesn't exist")
        return -1
    time.sleep(1)
    return 0

def remove(databse, clothes):
    return 0

def main():
    print ("starting the demo")
    database = []
    db.init_database(database)
    serialcomm = serial.Serial('/dev/cu.usbmodem1101', 9600)
    #serialcomm.timeout = 1

    add(database, "red")
    add(database, "blue")
    print_database(database)
    take(database, "red")
    print_database(database)
    add(database, "red")
    serialcomm.close()
    return 0


if __name__ == "__main__":
    main()


