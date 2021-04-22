from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator

app = Flask(__name__)
nav = Nav(app)

nav.register_element('my_navbar', Navbar('thenav', 
View('Home', 'index'), 
View('Add', 'add'), 
View('Remove', 'remove'),
View('Return', 'ret'),
View('Take', 'take')
))

@app.route("/")
def index():
    print("going to index.htm")
    return render_template("index.html")

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