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

@app.route("/add")
def add():
    if request.method == "POST":
        img_file = request.form["img"]
        # Henry this part is where you need to do the integration
        # type_of_clothes, color = post_request(img_file) 
        type_of_clothes = "tshirt"
        color = "blue"
        add(database, type_of_clothes, color)
        return redirect(url_for('waiting'))

        # Now we add this new clothes to the database

    else: 
        print("going to add.html")   
        return render_template("add.html")


# for remove clothes, I want to display database
@app.route("/remove")
def remove():
    print("going to remove.html")
    return render_template("remove.html", datab = database)

# This will be same as add except, we will redirect to 
# 1 additional page, which will require user feedback of clothes
@app.route("/ret")
def ret():
    print("going to ret.html")
    return render_template("ret.html")

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


@app.route("/update")
def update():
    print("going to update.html")
    return render_template("update.html")


def add(database, type_of_clothes, color):
    # add to database
    i = db.find_index_to_add(database)
    db.add_to_database(database, i, "tshirt", color)
    # after we add to database, we will rotate the servo
    sc.rotate_servo(i * 9)
    time.sleep(1)
    return 0



if __name__ == "__main__":
    print("starting smartwardrobe")
    db.init_database(database)
    db.print_database(database)
    #serialcomm = serial.Serial('/dev/cu.usbmodem1101', 9600)
    app.run(debug=True)
    