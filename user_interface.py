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
        # set the global variables here
        cur_type_of_clothes = "tshirt"
        cur_color = "blue"
        # we don't add clothes to the database here yet
        i = db.find_index_to_add(database)
        sc.rotate_servo(cur_angle, i * 9)
        return redirect(url_for('update_add'))

    else: 
        print("going to add.html")   
        return render_template("add.html")

@app.route("/update_add", methods=["POST", "GET"])
def update_add():
    if request.method == "POST":
        # here I will update the database
        preference = request.form["nm"]
        i = db.find_index_to_add(database)
        db.add_to_database(database, i, cur_type_of_clothes, cur_color, preference)
        cur_angle = i * 9
        return redirect(url_for('home'))

    else:
        print("going to update_add.html")
        return render_template("update_add.html")


# for remove clothes, I want to display database
@app.route("/remove", methods=["POST", "GET"])
def remove():
    if request.method == "POST":
        # Here the user will decide what clothes they would like to remove
        temp = request.form.getlist("remove")
        cur_color, cur_type_of_clothes = temp[0].split(" ")
        print(cur_color, cur_type_of_clothes)
        i = db.find_clothes_index(database, cur_type_of_clothes, cur_color)
        if i != -1:
            sc.rotate_servo(cur_angle, i * 9)
            return redirect(url_for('update_remove'))
        else:
            print ("couldn't find the clothes for some reason")
            return redirect(url_for('home'))

    else: 
        print("going to remove.html")   
        return render_template("remove.html", datab = database)

@app.route("/update_remove", methods=["POST", "GET"])
def update_remove():
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
    if request.method == "POST":
        img_file = request.form["img"]
        # call the visualizer API here with the img_file
        # type_of_clothes, color = visualizerapi(img_file) 
        cur_type_of_clothes = "tshirt"
        cur_color = "blue"
        # we don't add clothes to the database here yet
        i = db.find_index_to_add(database)
        sc.rotate_servo(cur_angle, i * 9)
        return redirect(url_for('update_ret'))

    else: 
        print("going to ret.html")   
        return render_template("ret.html")

@app.route("/update_ret", methods=["POST", "GET"])
def update_ret():
    if request.method == "POST":
        # here I will update the database
        preference = request.form["nm"]
        i = db.find_index_to_add(database)
        db.add_to_database(database, i, cur_type_of_clothes, cur_color, preference)
        cur_angle = i * 9
        return redirect(url_for('home'))

    else:
        print("going to update_ret.html")
        return render_template("update_ret.html")

# I will implement checkboxes
@app.route("/take", methods=["POST", "GET"])
def take():
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
        return redirect(url_for('show_take'))
        
        # It's ur turn to do the integration Hlin1
    else:   
        print("going to take.html")
        return render_template("take.html", class_lookup = class_lookup)

@app.route("/show_take", methods=["POST", "GET"])
def show_take():
    if request.method == "POST":
        # cur_type_of_clothes, cur_color = get_from_picture()
        i = db.find_clothes_index(database, cur_type_of_clothes, cur_color)
        if i != -1:
            sc.rotate_servo(cur_angle, i * 9)
            return redirect(url_for('update_take'))
        else:
            print ("couldn't find the clothes for some reason")
            return redirect(url_for('home'))
        
    else:
        # Here I will show all the pictures of clothes that I can choose from
        # Call the matching API
        # Call the preference API
        cur_type_of_clothes = "tshirt"
        cur_color = "red"
        return render_template("show_take.html")

@app.route("/update_take", methods=["POST", "GET"])
def update_take():
    if request.method == "POST":
        # here I will update the database
        i = db.find_clothes_index(database, cur_type_of_clothes, cur_color)
        db.remove_from_database(database, i)
        cur_angle = i * 9
        return redirect(url_for('home'))

    else:
        print("going to update_take.html")
        return render_template("update_take.html")

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
    