import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'/clothing_recognition'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'/clothing_recognition/detector'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'/clothing_recognition/classifier'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'/visualizer'))

from flask import Flask, render_template, redirect, url_for, request
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
import database.database as db
import matching as matching
# import retriever.servo_control as sc
import time
# import serial
from PIL import Image
import visualizer.visualizer as vi
# import fakeapi as vi
import user_preference.user_preference as up

app = Flask(__name__)
nav = Nav(app)

nav.register_element('my_navbar', Navbar('thenav', 
View('Home', 'home'), 
View('Add', 'add'), 
View('Remove', 'remove'),
View('Return', 'ret'),
View('Take', 'take')
))

database = []
cur_angle = 0
cur_type_of_clothes = ""
cur_color = ""
class_lookup = ["Anorak", "Blazer", "Blouse", "Bomber", "Button-Down", "Caftan", "Capris", "Cardigan", "Chinos", "Coat, Coverup", "Culottes", "Cutoffs", "Dress", "Flannel", "Gauchos", "Halter", "Henley", "Hoodie", "Jacket", "Jeans", "Jeggings", "Jersey", "Jodhurs", "Joggers", "Jumpsuit", "Kaftan", "Kimono", "Leggings", "Onesie", "Parka", "Peacoat", "Poncho", "Robe", "Romper", "Sarong", "Shorts", "Skirt", "Sweater", "Sweatpants", "Sweatshorts", "Tank", "Tee", "Top", "Trunks", "Turtleneck"]

final_clothes = []
final_color = []

db.init_database(database)
db.print_database(database)
vapi = vi.VisualizerAPI()
crm = vapi.clothingRecModel

clothes_combination_tuple = ()
clothes_option = []
global_clothes_information = []

next_type_of_clothes = ""
next_color = ""
clothes_taken_index_list = []

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home", methods=["POST", "GET"])
def home():
    global clothes_taken_index_list
    if request.method == "POST":
        type_of_action = request.form["nm"]
        print(type_of_action)
        return redirect(url_for(type_of_action))
    else: # request is get
        print("going to home.html")
        # need to make the array of inside_db_img
        imgs = db.create_home_display(database)
        print(imgs)
        #imgs = ["(0, 0, 0)Tee.jpeg", "(255, 0, 0)Jeans.jpeg"]
        return render_template("home.html", imgs = imgs)

@app.route("/add", methods=["POST", "GET"])
def add():
    global cur_type_of_clothes
    global cur_color
    global clothes_option

    if request.method == "POST":
        f = request.files["img"]
        print(f)
        # f.save("static/db_img", f)

        image = Image.open(f).convert("RGB")
        temp_labels, temp_colors = crm.getLabels(image)
        print(temp_labels[0], temp_colors[0])
        cur_type_of_clothes = temp_labels[0][0]

        cur_color = temp_colors[0]
        clothes_option = temp_labels[0]

        # cur_type_of_clothes = "tshirt"
        # cur_color = "red"
        
        # rename img_file
        img_name = str(cur_color) + cur_type_of_clothes + ".jpeg"
        # save this image file in db_img
        image.save(os.path.join("static/db_img", img_name), format="JPEG")
        #f.save("static/db_img/" + img_name)

        return redirect(url_for('confirm_add'))

    else: 
        print("going to add.html")   
        return render_template("add.html")

@app.route("/confirm_add", methods=["POST", "GET"])
def confirm_add():
    global cur_type_of_clothes

    if request.method == "POST":
        
        # first we check if clothes option is correct
        temp = request.form.getlist("correct")

        print("cur_type_of_clothes is " + cur_type_of_clothes)
        print("temp[0] which should be jacket is " + temp[0])
        
        if cur_type_of_clothes != temp[0]:
            print("image processing not successful")
            # the image procesing was not successful
            # we have to rename using os
            old_img_dir = "static/db_img/" + str(cur_color) + cur_type_of_clothes + ".jpeg"
            new_img_dir = "static/db_img/" + str(cur_color) + temp[0] + ".jpeg"
            os.rename(old_img_dir, new_img_dir)

            # now we will have to redefine cur_type_of_clothes to temp
            cur_type_of_clothes = temp[0]

        # we don't add clothes to the database here yet
        angle = db.find_angle_to_add(database)
        # sc.rotate_servo(cur_angle, angle)
        return redirect(url_for('update_add'))

    else: 
        print("going to confirm_add.html")   
        return render_template("confirm_add.html", clothes_option = clothes_option)


@app.route("/update_add", methods=["POST", "GET"])
def update_add():
    global database
    global cur_angle

    if request.method == "POST":
        # here I will update the database
        preference = request.form["nm"]
        if int(preference) < 5:
            preference = "-1"
        else:
            preference = "1"
        angle = db.find_angle_to_add(database)
        print("cur_type: ", cur_type_of_clothes)
        clothing_type = vi.VisualizerAPI.getClothingType(cur_type_of_clothes)
        db.add_to_database(database, angle, cur_type_of_clothes, cur_color, preference, clothing_type)
        cur_angle = angle
        return redirect(url_for('home'))

    else:
        print("going to update_add.html")
        return render_template("update_add.html")


# for remove clothes, I want to display database
@app.route("/remove", methods=["POST", "GET"])
def remove():
    global cur_type_of_clothes
    global cur_color

    if request.method == "POST":
        # Here the user will decide what clothes they would like to remove
        temp = request.form.getlist("remove")

        split_index = temp[0].find(")")
        cur_color_temp = temp[0][:split_index + 1]
        cur_color = db.convert_string_to_tuple(cur_color_temp)
        cur_type_of_clothes = temp[0][split_index + 2:]

        print("cur type of clothes is" + cur_type_of_clothes)
        angle = db.find_clothes_angle(database, cur_type_of_clothes, cur_color)
        if angle != -1:
            # sc.rotate_servo(cur_angle, angle)
            return redirect(url_for('update_remove'))
        else:
            print ("couldn't find the clothes for some reason")
            return redirect(url_for('home'))

    else: 
        print("going to remove.html")   
        return render_template("remove.html", datab = database)

@app.route("/update_remove", methods=["POST", "GET"])
def update_remove():
    global database
    global cur_angle
    if request.method == "POST":
        # here I will update the database
        angle = db.find_clothes_angle(database, cur_type_of_clothes, cur_color)
        if angle != -1:
            db.remove_from_database(database, i)
            cur_angle = angle
        else:
            print("this clothes can't be found from database")
        return redirect(url_for('home'))

    else:
        print("going to update_remove.html")
        return render_template("update_remove.html")

# changed the entire return function so that we will be returning the clothes 
# we took 
@app.route("/ret", methods=["POST", "GET"])
def ret():
    global clothes_taken_index_list

    if request.method == "POST":

        clothes_taken_index_list = db.find_clothes_taken(database)
        print ("clothes_taken_index_list is ")
        print (clothes_taken_index_list)
        #sc.rotate_servo(cur_angle, clothes_taken_index_list[0])
        return redirect(url_for('update_ret'))
    
    else:
        print("going to ret.html")
        return render_template("ret.html")


@app.route("/update_ret", methods=["POST", "GET"])
def update_ret():
    global database
    global cur_angle
    global clothes_combination_tuple

    if request.method == "POST":

        # get the preference for the user preference model
        preference = request.form["nm"]
        if int(preference) < 5:
            preference = "-1"
        else:
            preference = "1"

        i = clothes_taken_index_list[0]
        toc = database[i].type_of_clothes
        col = database[i].color
        db.return_to_database(database, i)
        
        clothes_combination_tuple = ((toc, toc, toc, toc, toc, col),)

        angle = database[i].angle

        if len(clothes_taken_index_list) == 2:
            # sc.rotate_servo(cur_angle, angle)
            cur_angle = angle
            return redirect(url_for('update_ret2'))
        # one clothes
        elif len(clothes_taken_index_list) == 1:
            cur_angle = angle
            up.setRating(preference, clothes_combination_tuple)  
            return redirect(url_for('home'))
        else:
            print("clothes taken index is wrong")
            return redirect(url_for('home'))
            
    else:
        print("going to update_ret.html")
        return render_template("update_ret.html")

@app.route("/update_ret2", methods=["POST", "GET"])
def update_ret2():
    global database
    global cur_angle

    if request.method == "POST":
        # get the preference for the user preference model
        preference = request.form["nm"]
        if int(preference) < 5:
            preference = "-1"
        else:
            preference = "1"

        i = clothes_taken_index_list[1]
        toc = database[i].type_of_clothes
        col = database[i].color
        db.return_to_database(database, i)

        angle = database[i].angle
        cur_angle = angle

        temp_tuple = ((toc, toc, toc, toc, toc, col),)
        final_tuple = clothes_combination_tuple + temp_tuple
        up.setRating(preference, final_tuple) 

        return redirect(url_for('home'))

        return redirect(url_for('home'))

    else:
        print("going to update_ret2.html")
        return render_template("update_ret2.html")

# I will implement checkboxes
@app.route("/take", methods=["POST", "GET"])
def take():
    global final_clothes
    global cur_color
    if request.method == "POST":
        final_clothes = request.form.getlist("type_of_clothes")
        r, g, b = request.form.get("red"), request.form.get("green"), request.form.get("blue")
        cur_color = (int(r), int(g), int(b))

        return redirect(url_for('show_take'))
    else:   
        print("going to take.html")
        return render_template("take.html", class_lookup = class_lookup)

@app.route("/show_take", methods=["POST", "GET"])
def show_take():
    global cur_type_of_clothes
    global cur_color
    global global_clothes_information
    global next_type_of_clothes
    global next_color

    if request.method == "POST":
        temp_0 = request.form.getlist("mycheckbox")
        print("temp_0 is")
        print(temp_0)
        temp = temp_0[0]
        print("temp is")
        print(temp)
        parse_index_0 = temp.find("/")
        parse_index_1 = temp.find("/", parse_index_0+1)
        parse_index_2 = temp.find(".")
        temp_index = int(temp[parse_index_1 + 1:parse_index_2])
        print(temp_index)

        # might need to use this one
        #temp = request.form.getlist("correct")
        temp_combination = global_clothes_information[temp_index]
        print(temp_combination)
        # now temp combination will contain the information about the clothes combination
        # we expect temp combination to be in this form
        # (("Tee", "Tee", "Tee", "Tee", "Tee",(0, 0, 0)), ("jeans", "jeans", "jeans", "jeans", "jeans", (255, 255, 255)))

        if len(temp_combination) == 2:
            # we will be taking 2 clothes
            cur_type_of_clothes = temp_combination[0][0]

            cur_color = temp_combination[0][5]

            next_type_of_clothes = temp_combination[1][0]
            next_color = temp_combination[1][5]

            angle = db.find_clothes_angle(database, cur_type_of_clothes, cur_color)
            if angle != -1:
                # sc.rotate_servo(cur_angle, angle)
                return redirect(url_for('update_take'))
            else:
                print ("couldn't find the clothes for 2 clothes (top) for some reason")
                return redirect(url_for('home'))
        
        else:
            # it will be a one piece clothing
            cur_type_of_clothes = temp_combination[0][0]
            cur_color = temp_combination[0][5]
            angle = db.find_clothes_angle(database, cur_type_of_clothes, cur_color)
            if angle != -1:
                # sc.rotate_servo(cur_angle, angle)
                return redirect(url_for('update_take2'))
            else:
                print ("couldn't find the clothes for one piece of clothing for some reason")
                return redirect(url_for('home'))
        
    else:
        # Call the matching API
        print(final_clothes, cur_color)
        clothes_to_take = matching.setFilter(final_clothes, cur_color, database)
        print("clothes to take: ", clothes_to_take)
        # Call the preference API using the clothes_to_take
        combinations = matching.getMatches(database, clothes_to_take)

        global_clothes_information = []

        # call the visualizerAPI using combinations
        # using these clothes combinations, we will get the corresponding images
        outfitImages = []
        filenames = []
        for combination in combinations:
            print(combination)
            outfitImages += vapi.getOutfitImgs(combination, 5)
            global_clothes_information += [combination for i in range(5)]
        
        # Here  we will be saving the files into jpeg
        for (index,image) in enumerate(outfitImages):
            filename = "static/take_img/" + str(index) + ".jpeg"
            image.save(filename, format="JPEG")
            filenames.append(filename)

        return render_template("show_take.html", imgs = filenames)

@app.route("/update_take", methods=["POST", "GET"])
def update_take():
    global database
    global cur_angle
    global cur_type_of_clothes
    global cur_color
    if request.method == "POST":
        # here I will update the database
        angle = db.find_clothes_angle(database, cur_type_of_clothes, cur_color)
        db.take_from_database(database, angle)
        cur_angle = angle
        cur_type_of_clothes = next_type_of_clothes
        cur_color = next_color

        angle = db.find_clothes_angle(database, cur_type_of_clothes, cur_color)
        if angle != -1:
            # sc.rotate_servo(cur_angle, angle)
            return redirect(url_for('update_take2'))
        else:
            print ("couldn't find the clothes for the bottom clothing for some reason")
            return redirect(url_for('home'))
        
        return redirect(url_for('update_take2'))

    else:
        print("going to update_take.html")
        return render_template("update_take.html")

@app.route("/update_take2", methods=["POST", "GET"])
def update_take2():
    global database
    global cur_angle
    if request.method == "POST":
        # here I will update the database
        angle = db.find_clothes_angle(database, cur_type_of_clothes, cur_color)
        db.take_from_database(database, angle)
        cur_angle = angle
        return redirect(url_for('home'))

    else:
        print("going to update_take2.html")
        return render_template("update_take2.html")

if __name__ == "__main__":
    #serialcomm = serial.Serial('/dev/cu.usbmodem1101', 9600)
    app.run(debug=True)