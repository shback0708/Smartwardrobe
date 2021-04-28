import database.database as db
import retriever.servo_control as sc
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
                final += [clothes]

    return final

# returns images of the best outfits 
# output_of_setFilter will be a 2D array
# output of getMatches will be all the images displayed to the user
# def getMatches(output_of_setFilter):

# we don't need this part because the rest 
# will be handled by the preferences model
    



