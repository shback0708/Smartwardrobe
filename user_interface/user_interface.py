from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    print("going to index.htm")
    return render_template("index.htm")

@app.route("/add")
def add():
    print("going to add.htm")
    return render_template("add.htm")

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
    return render_template("remove.htm")

@app.route("/ret")
def ret():
    return render_template("ret.htm")

@app.route("/take")
def take():
    return render_template("take.htm")

if __name__ == "__main__":
    app.run(debug=True)