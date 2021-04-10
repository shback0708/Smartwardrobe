# this angle will be from 0 to 180, incremented by 9 
database = []

class clothes:
    def __init__(self, angle, type_of_clothes, color):
        self.angle = angle
        self.type_of_clothes = type_of_clothes
        self.color = color 

def init_database(database):
    for i in range(20):
        database.append(clothes(-1, "", ""))
    return

def find_empty_angle_index(database):
    for i in range(len(database)):
        if database[i].angle == -1:
            return i

def add_to_database(database, index, type_of_clothes, color):
    database[i].angle = index * 9
    database[i].type_of_clothes = type_of_clothes
    database[i].color = color 
    return

def find_clothes_index(database, type_of_clothes, color):
    for i in range(len(database)):
        if database[i].type_of_clothes == type_of_clothes and database[i].color = color:
            return i
        else:
            return -1


def remove_from_database(database, index):
    database[index].angle = -1
    return