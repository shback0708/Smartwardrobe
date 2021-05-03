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
        for cloth in t:
            if cloth.angle != -1:
                final.append((cloth.type_of_clothes, cloth.type_of_clothes, cloth.type_of_clothes, cloth.type_of_clothes, cloth.type_of_clothes, cloth.color))
    for i in category:
        clothes = db.match_type(database, i)
        print("clothes: ", clothes)
        for cloth in clothes:
            if cloth not in final and cloth.angle != -1 and cloth.clothes_taken != True:
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
    likes = []
    neutral = []
    dislikes = []
    # find top and bottom combinations
    for top in tops:
        for bottom in bottoms:
            # TODO: preference integration

            #remove dupes
            if (top, bottom) not in outfits:
                outfits.append((top, bottom))
                rating = up.getRating((top, bottom))
                if rating == 1:
                    likes.append((top,bottom))
                elif rating == 0:
                    neutral.append((top,bottom))
                else:
                    dislikes.append((top,bottom))

    # just one-piece combinations
    for onePiece in onePieces:
        # TODO: preference integration

        #remove dupes
        if (onePiece) not in outfits:
            outfits.append((onePiece,))
            rating = up.getRating((onePiece,))
            if rating == 1:
                likes.append((onePiece,))
            elif rating == 0:
                neutral.append((onePiece,))
            else:
                dislikes.append((onePiece,))
    a = likes + neutral + dislikes
    return a
    #return outfits

#returns type of clothing
#0 for tops, 1 for bottoms, 2 for onepieces
def getClothingType(category):
    tops = ['Anorak', 'Blazer', 'Blouse', 'Bomber', 'Button-Down', 'Cardigan', 'Coat', 'Flannel', 'Halter', 'Henley', 'Hoodie', 'Jacket', 'Jersey', 'Parka', 'Peacoat', 'Poncho', 'Sweater',  'Tank', 'Tee', 'Top', 'Turtleneck']
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

if __name__ == '__main__':
    database = []
    db.init_database(database)
    db.add_to_database(database,0,"Coat",(0,0,0),0,0)
    db.add_to_database(database,1,"Coat",(0,0,300),0,0)
    db.add_to_database(database,2,"Jeans",(300,0,0),0,1)
    db.add_to_database(database,3,"Dress",(0,300,0),0,2)

    a = (("Coat","a","b","c","d",(0,0,0)), ("Jeans","a","b","c","d",(300,0,0)))
    b = (("Dress","a","b","c","d",(0,300,0)),)

    up.setRating(-1, a)
    up.setRating(-1,b)


    d = setFilter(("Coat","Jeans","Dress"),(0,0,0),database)
    print(d)
    print(getMatches(database,d))
    #print(getMatches(database,(b,c)))