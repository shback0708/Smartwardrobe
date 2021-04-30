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
import visualizer.webscraper as ws
import visualizer.visualizer as vi
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
cc = ""
vapi = ""
final_clothes = []
final_color = []

clothes_combination_string = ""
clothes_option = []

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        type_of_action = request.form["nm"]
        return redirect(url_for(type_of_action))
    else: # request is get
        print("going to home.html")
        # need to make the array of inside_db_img
        imgs = db.create_home_display(database)
        #imgs = ["redtshirt.jpg", "bluejeen.jpg"]
        return render_template("home.html", imgs = imgs)

@app.route("/add", methods=["POST", "GET"])
def add():
    global cur_type_of_clothes
    global cur_color
    global clothes_option

    if request.method == "POST":
        f = request.files["img"]

        image = Image.open(f).convert("RGB")
        temp_label, _, temp_color = cc.getAttributes(image)
        print(temp_label, temp_color)
        cur_type_of_clothes = temp_label[0]
        cur_color = webs.get_colour_name(temp_color)
        clothes_option = temp_label
        # cur_type_of_clothes = "tshirt"
        # cur_color = "red"
        
        # rename img_file
        img_name = cur_color + cur_type_of_clothes + ".jpg"
        # save this image file in db_img
        f.save(os.path.join("static/db_img", img_name))

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
        
        if cur_type_of_clothes != temp[0]:
            print("image processing not successful")
            # the image procesing was not successful
            # we have to rename using os
            old_img_dir = "static/db_img/" + cur_color + cur_type_of_clothes + ".jpg"
            new_img_dir = "static/db_img/" + cur_color + temp[0] + ".jpg"
            os.rename(old_img_dir, new_img_dir)

            # now we will have to redefine cur_type_of_clothes to temp
            cur_type_of_clothes = temp

        # we don't add clothes to the database here yet
        i = db.find_index_to_add(database)
        # sc.rotate_servo(cur_angle, i * 9)
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
        i = db.find_index_to_add(database)
        print("cur_type: ", cur_type_of_clothes)
        clothing_type = vi.VisualizerAPI.getClothingType(cur_type_of_clothes)
        db.add_to_database(database, i, cur_type_of_clothes, cur_color, preference, clothing_type)
        cur_angle = i * 9
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
        cur_color, cur_type_of_clothes = temp[0].split(" ")
        print(cur_color, cur_type_of_clothes)
        i = db.find_clothes_index(database, cur_type_of_clothes, cur_color)
        if i != -1:
            # sc.rotate_servo(cur_angle, i * 9)
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
        i = db.find_clothes_index(database, cur_type_of_clothes, cur_color)
        db.remove_from_database(database, i)
        cur_angle = i * 9
        return redirect(url_for('home'))

    else:
        print("going to update_remove.html")
        return render_template("update_remove.html")

# This will be same as add except, we will redirect to 
# 1 additional page, which will require user feedback of clothes
@app.route("/ret", methods=["POST", "GET"])
def ret():
    global cur_type_of_clothes
    global cur_color

    if request.method == "POST":
        img_file = request.form["img"]
        # This is where we get the color and type_of_clothes
        image = Image.open(img_file).convert("RGB")
        temp_label, _, temp_color = cc.getAttributes(image)
        cur_type_of_clothes = temp_label[0]
        cur_color = webs.get_colour_name(temp_color[0])
        # we don't add clothes to the database here yet
        i = db.find_index_to_add(database)
        # sc.rotate_servo(cur_angle, i * 9)
        return redirect(url_for('update_ret'))

    else: 
        print("going to ret.html")   
        return render_template("ret.html")

@app.route("/update_ret", methods=["POST", "GET"])
def update_ret():
    global database
    global cur_angle

    if request.method == "POST":
        # here I will update the database
        preference = request.form["nm"]
        if int(preference) < 5:
            preference = "-1"
        else:
            preference = "1"

        i = db.find_index_to_add(database)
        clothing_type = vapi.getClothingType(cur_type_of_clothes)
        db.add_to_database(database, i, cur_type_of_clothes, cur_color, preference, clothing_type)
        cur_angle = i * 9
        if clothing_type != 2:
            clothes_combination_string = cur_color + cur_type_of_clothes
            return redirect(url_for('ret2'))
        else:
            # Here we will update the combination
            clothes_combination_string = (cur_color + cur_type_of_clothes)
            up.setRating(preference, clothes_combination_string)
            return redirect(url_for('home'))

    else:
        print("going to update_ret.html")
        return render_template("update_ret.html")

# When we're returning clothes, we might be returning
# top and bottom at the same time
# This will deal with returning 2 clothes
# and asking for the preference
@app.route("/ret2", methods=["POST", "GET"])
def ret2():
    global cur_type_of_clothes
    global cur_color

    if request.method == "POST":
        img_file = request.form["img"]
        # This is where we get the color and type_of_clothes
        image = Image.open(img_file).convert("RGB")
        temp_label, temp_color = crm.getLabels(image)
        cur_type_of_clothes = temp_label[0][0]
        cur_color = webs.get_colour_name(temp_color[0])
        # we don't add clothes to the database here yet
        i = db.find_index_to_add(database)
        # sc.rotate_servo(cur_angle, i * 9)
        return redirect(url_for('update_ret2'))

    else: 
        print("going to ret2.html")   
        return render_template("ret2.html")

@app.route("/update_ret2", methods=["POST", "GET"])
def update_ret2():
    global database
    global cur_angle

    if request.method == "POST":
        # here I will update the database
        preference_for_combination = request.form["nm"]
        if int(preference) < 5:
            preference = "-1"
        else:
            preference = "1"

        i = db.find_index_to_add(database)
        clothing_type = vapi.getClothingType(cur_type_of_clothes)
        db.add_to_database(database, i, cur_type_of_clothes, cur_color, 5, clothing_type)
        cur_angle = i * 9
        # Here we will update the combination
        clothes_combination_string += (cur_color + cur_type_of_clothes)
        up.setRating(preference, clothes_combination_string)  
        return redirect(url_for('home'))

    else:
        print("going to update_ret2.html")
        return render_template("update_ret2.html")

# I will implement checkboxes
@app.route("/take", methods=["POST", "GET"])
def take():
    global final_color
    global final_clothes
    if request.method == "POST":
        clothes = request.form.get("type_of_clothes")
        cl = clothes.split("clothes=")
        final_clothes = []
        for c in cl:
            if c[-1] == '&':
                final_clothes += [c[:-1]]
            else:
                final_clothes += [c]
        r, g, b = request.form["red"], request.form["green"], request.form["blue"]
        final_color = [int(r), int(g), int(b)]
        print(final_color)
        return redirect(url_for('show_take'))
    else:   
        print("going to take.html")
        return render_template("take.html", class_lookup = class_lookup)

@app.route("/show_take", methods=["POST", "GET"])
def show_take():
    global cur_type_of_clothes
    global cur_color

    if request.method == "POST":
        # cur_type_of_clothes, cur_color = get_from_picture()
        i = db.find_clothes_index(database, cur_type_of_clothes, cur_color)
        if i != -1:
            # sc.rotate_servo(cur_angle, i * 9)
            return redirect(url_for('update_take'))
        else:
            print ("couldn't find the clothes for some reason")
            return redirect(url_for('home'))
        
    else:
        # convert [R, G, B] into nearest color
        nearest_color = webs.get_colour_name(final_color)
        # Call the matching API
        print(final_clothes, nearest_color)
        clothes_to_take = matching.setFilter(final_clothes, nearest_color, database)
        print("clothes to take: ", clothes_to_take)
        # Call the preference API using the clothes_to_take
        combinations = matching.getMatches(database, clothes_to_take)

        # combinations here will be a set of strings that will look like
        #("blueshirtredpants", "whitejacketbluejeans")

        # call the visualizerAPI using combinations
        # using these clothes combinations, we will get the corresponding image
        outfitImages = []
        for clothes_img in combinations:
            print(clothes_img)
            outfitImages += [vapi.getOutfitImgs(clothes_img.type_of_clothes, clothes_img.color, 5)]
        return render_template("show_take.html", imgs = outfitImages)

@app.route("/update_take", methods=["POST", "GET"])
def update_take():
    global database
    global cur_angle
    if request.method == "POST":
        # here I will update the database
        i = db.find_clothes_index(database, cur_type_of_clothes, cur_color)
        db.remove_from_database(database, i)
        cur_angle = i * 9
        return redirect(url_for('home'))

    else:
        print("going to update_take.html")
        return render_template("update_take.html")

if __name__ == "__main__":
    print("starting smartwardrobe")
    db.init_database(database)
    db.print_database(database)
    cur_angle = 0
    vapi = vi.VisualizerAPI()
    cc = vapi.clothingRecModel.classifier
    webs = ws.WebScraper()
    #serialcomm = serial.Serial('/dev/cu.usbmodem1101', 9600)
    app.run(debug=True)
    