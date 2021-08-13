import os
from flask import (
    Flask, flash, render_template,
    redirect, jsonify, request, session, url_for)
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

ALL_SLOTS = ['10:00-11:00', '11:00-12:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00']
NEW_USER_ACCOUNT_TYPE = 'new_user'


def is_user_logged_in():
    if session.get("user"):
        return True
    return False


def get_user_account_type():
    account_type = mongo.db.users.find_one({'username': session["user"]})['account_type']
    return account_type


def get_users():
    users = list(mongo.db.users.find().sort("username", 1))
    return users


@app.route("/")
@app.route("/home")
def home():
    if is_user_logged_in():
        account_type = get_user_account_type()
    else:
        account_type = NEW_USER_ACCOUNT_TYPE
    return render_template('home.html', account_type=account_type)


@app.route("/register", methods=["GET", "POST"])
def register():
    # If logged in, redirect to home
    if is_user_logged_in():
        return redirect(url_for("home"))

    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        password = request.form.get("password")
        confirmPassword = request.form.get("confirm-password")

        if password != confirmPassword:
            flash("Your passwords do not match")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "phone_number": request.form.get("phone-number"),
            "email": request.form.get("email"),
            "account_type": "customer",
        }

        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username")
        session["account_type"] = request.form.get("account_type")
        flash("Registration Successful!")
        return redirect(url_for("view_bookings", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If logged in, redirect to home
    if is_user_logged_in():
        return redirect(url_for("home"))

    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("home", username=session["user"], account_type=get_user_account_type()))

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
    return redirect(url_for("login"))


@app.route("/booking/create", methods=["GET", "POST"])
def book_lesson():
    # this is a list of the bookable times to the user to compare to what is already booked in the database. in the future it will be able to be set by the instructor and fetched from the database.
    if not is_user_logged_in():
        return redirect(url_for("login"))
         # checks if user is logged in
    instructors = list(mongo.db.users.find({"account_type": "instructor"}))  # Gets list of users to get the driving instructor select input
    
    if request.method == "POST":
        booking = {
            'instructor': request.form.get("instructor").lower(),
            'student': session['user'],
            'date': request.form.get("date"),
            'time_slot': request.form.get('time_slot'),
            'optional_details': request.form.get('optional_details')
          }
        mongo.db.bookings.insert_one(booking)
        flash('Booking Succesfull')
    return render_template('bookLesson.html', instructors=instructors, account_type=get_user_account_type())


@app.route("/get_available_slots")
def get_available_slots():
    booking = {
      'date': request.args.get("date", ""),
      "instructor": request.args.get("instructor", "")
    }

    booked_slots = []
    available_slots = ALL_SLOTS

    existing_bookings = mongo.db.bookings.find(booking, {"_id": 0, 'time_slot': 1})
    for existing_booking in existing_bookings:
        booked_slots.append(existing_booking['time_slot'])   # querying the db and retreiving what times have been booked for the selected instructor on the selected day.

    if len(booked_slots) < len(available_slots):  # This is removing the booked times from the all times list which will then get sent to Driving lesson times

        available_slots = [item for item in available_slots if item not in booked_slots]

    else:
        flash('Fully Booked')    # if all times are booked it will return fully booked.

    return jsonify({"slots": available_slots})


@app.route("/bookings")
def view_bookings():
    if not is_user_logged_in():
        return redirect(url_for("login"))

    username = session["user"]
    bookings = list(mongo.db.bookings.find({'student': username},{'_id': 0}))

    return render_template("view_bookings.html", username=username, bookings=bookings, account_type=get_user_account_type())


@app.route("/booking/calender", methods=["GET", "POST"])
def booking_calender():
    if not is_user_logged_in():
        return redirect(url_for("login"))

    username = session["user"]
    user_account_type = mongo.db.users.find_one({"username": username})["account_type"]
    bookings = []
    if user_account_type == 'admin':
        bookings = list(mongo.db.bookings.find({}, {'_id': 0}))

    else:
        bookings = list(mongo.db.bookings.find({'instructor': username},{'_id': 0}))

    return render_template("bookingCalender.html", username=username, bookings=bookings, account_type=get_user_account_type())


@app.route("/users/manage", methods=["GET", "POST"])
def user_manager():
    users = get_users()
    return render_template("userManager.html", users=users, account_type=get_user_account_type())


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    users = list(mongo.db.users.find({"$text": {"$search": query}}))
    return render_template("userManager.html", users=users, account_type=get_user_account_type())


@app.route("/user/<user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    if request.method == "POST":
        current_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        submit = {
            "username": request.form.get("username").lower(),
            'password': current_user['password'],
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "phone_number": request.form.get("phone-number"),
            "email": request.form.get("email"),
            "account_type": request.form.get("account_type"),
        }
        mongo.db.users.update({"_id": ObjectId(user_id)}, submit)
        flash("User profile Successfully Updated")
        return redirect(url_for("userManager"))

    users = list(mongo.db.users.find().sort("username", 1))
    return render_template("userManager.html", users=users, account_type=get_user_account_type())


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")),
    debug=True)