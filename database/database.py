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

# def find_empty_angle_index(database):
#     for i in range(len(database)):
#         if database[i].angle == -1:
#             return i

''' 
0 -> [0,-5]
1 -> [1, -4]
2 -> [2, -3]
3 -> [3,-2]
4 -> [4,-1]
5 -> [5,0]
6 -> [4, 1]
continued on like this trend
'''
def convert_index_to_coordinate(index):
    x = 0
    y = 0
    if index <= 10:
        if index <= 5:
            x = index
            y = index - 5
        else:
            x = 10 - index
            y = index - 5
    else:
        if index <= 15:
            x = -(index - 10)
            y = 15 - index
        else:
            x = 20 - index
            y = 15 - index

    return [x,y]

def find_index_to_add(database):
    #find the center of mass in the database
    com = [0,0]
    temp = []
    for i in range(len(database)):
        if database[i].angle != -1:
            [x,y] = convert_index_to_coordinate(i)
            com[0] += x
            com[1] += y
        else:
            temp += [i]
    
    # now we have center of mass
    # we will go through temp, find coordinate of index furthest from temp
    # and then that will be our insertion index
    max_dist = 0
    max_index = 0
    for i in temp:
        [x_temp, y_temp] = convert_index_to_coordinate(i)
        dist = ((com[0] - x_temp) ** 2) + ((com[1] - y_temp) **2)
        if dist > max_dist:
            max_dist = dist
            max_index = i

    return max_index

def add_to_database(database, i, type_of_clothes, color):
    database[i].angle = i * 9
    database[i].type_of_clothes = type_of_clothes
    database[i].color = color 
    return

def find_clothes_index(database, type_of_clothes, color):
    for i in range(len(database)):
        if ((database[i].type_of_clothes == type_of_clothes) and (database[i].color == color)):
            return i
        else:
            return -1

def match_type_or_color(database, type_of_clothes, color):
    for i in range(len(database)):
        if ((database[i].type_of_clothes == type_of_clothes) or (database[i].color == color)):
            return database[i]
        else:
            return -1

def remove_from_database(database, index):
    database[index].angle = -1
    database[index].type_of_clothes = "removed"
    database[index].color = "removed"
    return