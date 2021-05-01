import database.database as db
import user_preference.user_preference as up
import time
# This will be the stub file for matching api



# we get the categories of clothes, and the colors of clothes
# category and clothes will be lists

# user inputed specs like jeans-only or black top
# This function will call the database and return all the combinations

def setFilter(category, color, database):
    final = set()
    t = db.match_color(database, color)
    if(t != []):
        final.add(t[0].color + "," + t[0].type_of_clothes)
    for i in category:
        clothes = db.match_type(database, i)
        print("clothes: ", clothes)
        for cloth in clothes:
            final.add(cloth.color + "," + cloth.type_of_clothes)
    return final

# returns images of the best outfits 
# output_of_setFilter will be a 2D array
# output of getMatches will be all the images displayed to the user
# final will look like [[]]
def getMatches(database, output_of_setFilter):
    final = []
    good_rating = []
    no_rating = []
    bad_rating = []
    for c in output_of_setFilter:
        temp = ()
        color, type_of_clothes = c.split(",")
        # color will be "(0,0,0)" and type of clothes will be "tshirt"
        clothing_type = getClothingType(type_of_clothes)
        temp_set = db.convert_string_to_set(color)
        # this means it's a top
        # we need to add suggestions for the bottom
        if clothing_type == 0:
            temp.append((type_of_clothes, "a", "b", "c", "d", temp_set))
            # finish it up by adding top and bottom combo to the temp
            for clothes in database:
                if clothes.clothing_type == 1:
                    temp_string = color + type_of_clothes
                    temp_string += clothes.color
                    temp_string += clothes.type_of_clothes
                    rating = up.getRating(temp_string)
                    temp.append((clothes.type_of_clothes, "a", "b", "c", "d", clothes.color))
                    if rating == -1:
                        bad_rating.append(temp)
                    elif rating == 0:
                        no_rating.append(temp)
                    elif rating == 1:
                        good_rating.append(temp)

        # bottom
        elif clothing_type == 1:
            # finish it up by adding top and bottom combo to the temp
            for clothes in database:
                if clothes.clothing_type == 0:      
                    temp_string = clothes.color
                    temp_string += clothes.type_of_clothes
                    temp_string += (color + type_of_clothes)
                    rating = up.getRating(temp_string)
                    temp.append((clothes.type_of_clothes, "a", "b", "c", "d", clothes.color))
                    temp.append((type_of_clothes, "a", "b", "c", "d", temp_set))
                    if rating == -1:
                        bad_rating.append(temp)
                    elif rating == 0:
                        no_rating.append(temp)
                    elif rating == 1:
                        good_rating.append(temp)


        # This means it's one piece, check preference immediately    
        elif clothing_type == 2:
            temp = color + type_of_clothes
            rating = up.getRating(temp)
            temp.append((type_of_clothes, "a", "b", "c", "d", temp_set))
            if rating == -1:
                bad_rating.append(temp)
            elif rating == 0:
                no_rating.append(temp)
            elif rating == 1:
                good_rating.append(temp)
        else:
            print("there's something wrong here")
    
    final = good_rating + no_rating + bad_rating
    return final


#returns type of clothing
#0 for tops, 1 for bottoms, 2 for onepieces
def getClothingType(category):
    tops = ['Anorak', 'Blazer', 'Bomber', 'Button-Down', 'Cardigan', 'Coat', 'Flannel', 'Halter', 'Henley', 'Hoodie', 'Jacket', 'Jersey', 'Parka', 'Peacoat', 'Poncho', 'Sweater',  'Tank', 'Tee', 'Top', 'Turtleneck']
    bottoms = ['Capris', 'Chinos', 'Culottes', 'Cutoffs', 'Gauchos', 'Jeans', 'Jeggings', 'Jodhpurs', 'Joggers', 'Leggings', 'Sarong', 'Shorts', 'Skirt', 'Sweatpants', 'Sweatshorts', 'Trunks']
    onepieces = ['Caftan', 'Coverup', 'Dress', 'Jumpsuit', 'Kaftan', 'Kimono', 'Onesie', 'Robe', 'Romper']
    if category in tops:
        return 0
    elif category in bottoms:
        return 1
    elif category in onepieces:
        return 2
    else:
        raise Exception("unknown clothing type: " + category)
