import database.database as db
import user_preference.user_preference as up
import time
# This will be the stub file for matching api



# we get the categories of clothes, and the colors of clothes
# category and clothes will be lists

# user inputed specs like jeans-only or black top
# This function will call the database and return all the combinations

def setFilter(category, color, database):
    final = []
    t = db.match_color(database, color)
    if(t != []):
        final.append((t[0].type_of_clothes, t[0].type_of_clothes, t[0].type_of_clothes, t[0].type_of_clothes, t[0].type_of_clothes, t[0].color))
    for i in category:
        clothes = db.match_type(database, i)
        print("clothes: ", clothes)
        for cloth in clothes:
            final.append((cloth.type_of_clothes, cloth.type_of_clothes, cloth.type_of_clothes, cloth.type_of_clothes, cloth.type_of_clothes, cloth.color))
    return final

# returns images of the best outfits 
# output_of_setFilter will be a 2D array
# output of getMatches will be all the images displayed to the user
# final will look like [[]]
def getMatches(database, clothes):

    # seperate clothes in categories
    tops = []
    bottoms = []
    onePieces = []
    # clothing is ((0,0,0), "Tee")
    for clothing in clothes:
        category = getClothingType(clothing[1])
        if category == 0: # top
            tops.append(clothing)
        elif category == 1: # bottom
            bottoms.append(clothing)
        else:
            onePieces.append(clothing)
    
    outfits = []
    # find top and bottom combinations
    for top in tops:
        for bottom in bottoms:
            # TODO: preference integration
            outfits.append((top, bottom))

    # just one-piece combinations
    for onePiece in onePieces:
        # TODO: preference integration
        outfits.append((onePiece))

    return outfits

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
