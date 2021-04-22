from flask import Flask, render_template, redirect, url_for, request
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator

app = Flask(__name__)
nav = Nav(app)

nav.register_element('my_navbar', Navbar('thenav', 
View('Home', 'home'), 
View('Add', 'add'), 
View('Remove', 'remove'),
View('Return', 'ret'),
View('Take', 'take')
))

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
    print("going to add.html")
    return render_template("add.html")

# @app.route("/add/clothes")
# def add_clothes():
#     # Actually here, user can input pictures and we can just call the visualizer
#     # api with that picture 
#     # they will have bunch of buttons they can select from
#     # look up the database for empty location (id = #)
#     # add to the emtpy location
#     userRequest(id)


@app.route("/remove")
def remove():
    print("going to remove.html")
    return render_template("remove.html")

@app.route("/ret")
def ret():
    print("going to ret.html")
    return render_template("ret.html")

@app.route("/take")
def take():
    print("going to take.htnml")
    return render_template("take.html")

if __name__ == "__main__":
    app.run(debug=True)