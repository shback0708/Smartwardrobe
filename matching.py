import database.database as db
import user_preference.user_preference as up
import time
# This will be the stub file for matching api


# we get the categories of clothes, and the colors of clothes
# category and clothes will be lists

# user inputed specs like jeans-only or black top
# This function will call the database and return all the combinations

def setFilter(category, color):
    final = []
    for i in category:
        clothes = db.match_type_or_color(i,color)
        if clothes != -1:
            if clothes != final:
                final += [clothes.color + "," + clothes.type_of_clothes]

    return final

# returns images of the best outfits 
# output_of_setFilter will be a 2D array
# output of getMatches will be all the images displayed to the user
# final will look like [[]]
def getMatches(vapi, database, output_of_setFilter):
    good_rating = set()
    no_rating = set()
    bad_rating = set()
    for c in output_of_setFilter:
        color, type_of_clothes = c.split(",")
        clothing_type = vapi.getClothingType(type_of_clothes)
        # this means it's a top
        # we need to add suggestions for the bottom
        if clothing_type == 0:
            # finish it up by adding top and bottom combo to the temp
            for clothes in database:
                if clothes.clothing_type == 1:
                    temp = color + type_of_clothes
                    temp += clothes.color
                    temp += clothes.type_of_clothes
                    rating = up.getRating(temp)
                    if rating == -1:
                        bad_rating.add(temp)
                    elif rating == 0:
                        no_rating.add(temp)
                    elif rating == 1:
                        good_rating.add(temp)

        # bottom
        elif clothing_type == 1:
            # finish it up by adding top and bottom combo to the temp
            for clothes in database:
                if clothes.clothing_type == 0:      
                    temp = clothes.color
                    temp += clothes.type_of_clothes
                    temp += (color + type_of_clothes)
                    rating = up.getRating(temp)
                    if rating == -1:
                        bad_rating.add(temp)
                    elif rating == 0:
                        no_rating.add(temp)
                    elif rating == 1:
                        good_rating.add(temp)


        # This means it's one piece, check preference immediately    
        elif clothing_type == 2:
            temp = color + type_of_clothes
            rating = up.getRating(temp)
            if rating == -1:
                bad_rating.add(temp)
            elif rating == 0:
                no_rating.add(temp)
            elif rating == 1:
                good_rating.add(temp)
        else:
            print("there's something wrong here")
    
    good_rating.update(no_rating)
    good_rating.update(bad_rating)
    return good_rating



    # use output_of_setFilter to find every single clothing combination

    # make sure to call getFilter to organize the combination

    return final


