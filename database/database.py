from diskcache import Cache

colorThreshold = 0.3
# this angle will be from 0 to 180, incremented by 9 
storage = Cache("storage")
class clothes:
    def __init__(self, angle, type_of_clothes, color, preference, clothing_type, clothes_taken = False):
        self.angle = angle
        self.type_of_clothes = type_of_clothes
        # color is now a tuple 
        self.color = color
        self.preference = 0
        self.clothing_type = -1
        self.clothes_taken = True

def init_database(database):
    for i in range(18):
        database.append(clothes(-1, "Tee", (0,0,0), 10, 0, True))
    database.append(clothes(18, "Tee", (0,0,255), 10, 0, True))
    database.append(clothes(19, "Jeans", (0,0,255), 10, 0, True))

    for i in range(20):
        if storage.get(str(i)) != None:
            database[i] = storage.get(str(i))
    return

def print_database(database):
    for clothes in database:
        print(clothes.angle, clothes.type_of_clothes, clothes.color, clothes.preference, clothes.clothing_type, clothes.clothes_taken)
    return

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

def add_to_database(database, i, type_of_clothes, color, preference, clothing_type):
    database[i].angle = i * 9
    database[i].type_of_clothes = type_of_clothes
    database[i].color = color 
    database[i].preference = preference
    database[i].clothing_type = clothing_type
    database[i].clothes_taken = False
    storage[str(i)] = database[i]
    return

def find_clothes_index(database, type_of_clothes, color):
    print(type_of_clothes, color)
    for i in range(len(database)):
        if ((database[i].type_of_clothes == type_of_clothes) and (colorError(database[i].color, color) <= colorThreshold)):
            return i
        else:
            return -1

def match_type_or_color(database, type_of_clothes, color):
    final = []
    for i in range(len(database)):
        if ((database[i].type_of_clothes == type_of_clothes) or (colorError(database[i].color, color) <= colorThreshold)):
            final.append(database[i])
    return final

def match_type(database, type_of_clothes):
    final = []
    for i in range(len(database)): 
        if ((database[i].type_of_clothes == type_of_clothes)):
            final.append(database[i])
    return final

def match_color(database, color):
    final = []
    for i in range(len(database)):   
        if ((colorError(database[i].color, color) <= colorThreshold)):
            final.append(database[i])
    return final

def create_home_display(database):
    final = []
    for clothes in database:
        if clothes.angle != 1:
            temp = "static/db_img/" + str(clothes.color) + clothes.type_of_clothes + ".jpeg"
            final.append(temp)
    return final

def remove_from_database(database, index):
    database[index].angle = -1
    database[index].type_of_clothes = "clothes is removed"
    database[index].color = "empty..."
    database[index].preference = 0
    database[index].clothing_type = -1
    database[index].clothes_taken = True
    storage[str(index)] = database[index]
    return

def take_from_database(database, index):
    if(database[index].clothes_taken == False):
        database[index].clothes_taken = True
        storage[str(index)] = database[index]
        return True
    return False

def return_to_database(database, index):
    database[index].clothes_taken = False
    storage[str(index)] = database[index]

# final can max be 2
def find_clothes_taken(database):
    final = []
    for i in range(len(database)):
        print(database[i])
        if ((database[i].clothes_taken == True) and (database[i].angle >= 0)):
            final.append(i)

    return final


def colorError(c1, c2):
    print(c1,c2)
    error = 0
    for i in range(3):
        error += ((c1[i] - c2[i]) / 255) ** 2 
    # normalization (0 - 1)
    error /= 3
    if error < 0 or error > 1:
        print(1/0)
    return error

def convert_string_to_tuple(input):
    # "(0,0,0)"
    temp = input[1:-1]
    # now it will be from
    comma_index1 = input.find(',')
    comma_index2 = input.find(',', comma_index1 + 1)
    r = input[1:comma_index1]
    g = input[comma_index1 + 2:comma_index2]
    b = input[comma_index2 + 2 :-1]
    return (int(r),int(g),int(b))

if __name__ == '__main__':
    db = []
    init_database(db)
    add_to_database(db,0,"tee","red",0,1)
    add_to_database(db,1,"tee","black",0,1)
    print(db[1].clothes_taken)
    take_from_database(db,1)
    print(db[1].clothes_taken)
    return_to_database(db,1)
    print(db[1].clothes_taken)

    #def add_to_database(database, i, type_of_clothes, color, preference, clothing_type):