from flask import Flask, render_template, redirect, url_for, request
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
import database.database as db
import retriever.servo_control as sc
import time
import serial

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
        return render_template("home.html")

@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        img_file = request.form["img"]
        # Henry this part is where you need to do the integration
        # type_of_clothes, color = post_request(img_file) 
        cur_type_of_clothes = "tshirt"
        cur_color = "blue"
        # we don't add clothes to the database here yet
        # add(database, type_of_clothes, color)
        return redirect(url_for('update_add'))

        # Now we add this new clothes to the database

    else: 
        print("going to add.html")   
        return render_template("add.html")

@app.route("/update_add", methods=["POST", "GET"])
def update_add():
    if request.method == "POST":
        # here I will update the database
        preference = request.form["nm"]
        add_to_db(database, cur_type_of_clothes, cur_color, preference)
        return redirect(url_for('home'))
    else:
        print("going to update_add.html")
        return render_template("update_add.html")


# for remove clothes, I want to display database
@app.route("/remove")
def remove():
    print("going to remove.html")
    return render_template("remove.html", datab = database)

# This will be same as add except, we will redirect to 
# 1 additional page, which will require user feedback of clothes
@app.route("/ret", methods=["POST", "GET"])
def ret():
    print("going to ret.html")
    if request.method == "POST":
        img_file = request.form["img"]
        # Henry this part is where you need to do the integration
        # type_of_clothes, color = post_request(img_file) 
        cur_type_of_clothes = "tshirt"
        cur_color = "blue"
        add(database, type_of_clothes, color)
        return redirect(url_for('update'))

        # Now we add this new clothes to the database

    else: 
        print("going to add.html")   
        return render_template("ret.html")

@app.route("/update_ret", methods=["POST", "GET"])
def update_ret():
    if request.method == "POST":
        # here I will update the database
        preference = request.form["nm"]
        add_to_db(database, cur_type_of_clothes, cur_color, preference)
        return redirect(url_for('home'))
    else:
        print("going to update_ret.html")
        return render_template("update_ret.html")

# I will implement checkboxes
@app.route("/take")
def take():
    print("going to take.html")
    if request.method == "POST":
        clothes = request.form["clothes"]
        cl = clothes.split("clothes=")
        finalClothes = []
        for c in cl:
            if c[-1] == '&':
                finalClothes += [c[:-1]]
            else:
                finalClothes += [c]
        r, g, b = request.form("red"), request.form("green"), request.form("blue")
        finalClothes += [r, g, b]
        
        # It's ur turn to do the integration Hlin1
        
    return render_template("take.html", class_lookup = class_lookup)


def add_to_db(database, type_of_clothes, color, preference):
    # add to database
    i = db.find_index_to_add(database)
    db.add_to_database(database, i, type_of_clothes, color, preference)
    # after we add to database, we will rotate the servo
    sc.rotate_servo(cur_angle, i * 9)
    # update the cur_angle
    cur_angle = i * 9
    return 0

def remove_from_db(database, type_of_clothes, color):
    # remove from database 
    i = db.find_clothes_index(database, type_of_clothes, color)
    db.remove_from_database(database, i)
    if i != -1:
        sc.rotate_servo(i * 9)
        # update the cur_angle
        cur_angle = i * 9
    else:
        print ("given clothes spec doesn't exist")
        return -1
    time.sleep(1)
    return 0

if __name__ == "__main__":
    print("starting smartwardrobe")
    db.init_database(database)
    db.print_database(database)
    cur_angle = 0
    #serialcomm = serial.Serial('/dev/cu.usbmodem1101', 9600)
    app.run(debug=True)
    