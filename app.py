import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        print("hi")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirm-password")

        if password != confirmPassword:
            flash("Your passwords do not match")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "firstName": request.form.get("first_name"),
            "lastName": request.form.get("last_name"),
            "phoneNumber": request.form.get("phone-number"),
            "email": request.form.get("email"),
            "accountType": "user",
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username")
        session["accountType"] = request.form.get("accountType")
        flash("Registration Successful!")
        return redirect(url_for("viewBookings", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                session["accountType"] = mongo.db.users.find_one({'username': session["user"]})['accountType']
                flash("Welcome, {}".format(request.form.get("username")))
                print(session['accountType'])
                print(session['user'])
                return redirect(url_for("viewBookings", username=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    session.pop("accountType")
    return redirect(url_for("login"))


@app.route("/view-bookings/<username>", methods=["GET", "POST"])
def viewBookings(username):
    username = session["user"]

    if session["user"]:
        return render_template("viewBookings.html", username=username)

    return redirect(url_for("login"))


@app.route("/bookLesson/<username>", methods=["GET", "POST"])
def bookLesson(username):
    username = session["user"]

    if session["user"]:
        return render_template("bookLesson.html", username=username)

    return redirect(url_for("login"))


@app.route("/bookingCalender/<username>", methods=["GET", "POST"])
def bookingCalender(username):
    username = session["user"]

    if session["user"]:
        return render_template("bookingCalender.html", username=username)

    return redirect(url_for("login"))


@app.route("/userManager", methods=["GET", "POST"])
def userManager():
    users = list(mongo.db.users.find())
    return render_template("userManager.html", users=users)




@app.route("/get_users")
def get_users():
    users = list(mongo.db.users.find().sort("username", 1))
    return render_template("userManager.html", users=users)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    users = list(mongo.db.users.find({"$text": {"$search": query}}))
    return render_template("userManager.html", users=users)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")),
    debug=True)
