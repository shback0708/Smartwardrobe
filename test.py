import sys
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
import database.database as db
import time
# import serial
#from PIL import Image

app = Flask(__name__)
nav = Nav(app)

# picFolder = os.path.join('static', 'db_img')
# app.config['UPLOAD_FOLDER'] = picFolder

nav.register_element('my_navbar', Navbar('thenav', 
View('Home', 'home'), 
View('Add', 'add'), 
View('Remove', 'remove'),
View('Return', 'ret'),
View('Take', 'take')
))
database = []
clothes_option = []

class_lookup = ["Anorak", "Blazer", "Blouse", "Bomber", "Button-Down", "Caftan", "Capris", "Cardigan", "Chinos", "Coat, Coverup", "Culottes", "Cutoffs", "Dress", "Flannel", "Gauchos", "Halter", "Henley", "Hoodie", "Jacket", "Jeans", "Jeggings", "Jersey", "Jodhurs", "Joggers", "Jumpsuit", "Kaftan", "Kimono", "Leggings", "Onesie", "Parka", "Peacoat", "Poncho", "Robe", "Romper", "Sarong", "Shorts", "Skirt", "Sweater", "Sweatpants", "Sweatshorts", "Tank", "Tee", "Top", "Trunks", "Turtleneck"]

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

        cur_type_of_clothes = "tshirt"
        cur_color = "green"

        img_name = cur_color + cur_type_of_clothes + ".jpg"
        # save this image file in db_img
        f.save(os.path.join("static/db_img", img_name))

        clothes_option = ["tshirt", "jacket"]

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
    return render_template("update_add.html")

@app.route("/remove", methods=["POST", "GET"])
def remove():
    return render_template("remove.html")

@app.route("/ret", methods=["POST", "GET"])
def ret():
    return render_template("ret.html")

@app.route("/take", methods=["POST", "GET"])
def take():
    if request.method == "POST":
        clothes = request.form["clothes"]
        cl = clothes.split("clothes=")
        final_clothes = []
        for c in cl:
            if c[-1] == '&':
                final_clothes += [c[:-1]]
            else:
                final_clothes += [c]
        r, g, b = request.form("red"), request.form("green"), request.form("blue")
        final_color += [r, g, b]
        return redirect(url_for('show_take'))
    else:   
        print("going to take.html")
        return render_template("take.html", class_lookup = class_lookup)

if __name__ == "__main__":
    print("starting smartwardrobe")
    db.init_database(database)
    db.print_database(database)
    cur_angle = 0
    #vapi = vi.VisualizerAPI()
    #cc = vapi.clothingRecModel.classifier
    # webs = ws.WebScraper()
    #serialcomm = serial.Serial('/dev/cu.usbmodem1101', 9600)
    app.run(debug=True)