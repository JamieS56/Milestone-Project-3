import os
from flask import (
    Flask, flash, render_template,
    redirect, jsonify, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

ALL_SLOTS = ['10:00-11:00', '11:00-12:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00']      # this is a list of the bookable times to the user to compare to what is already booked in the database. in the future it will be able to be set by the instructor and fetched from the database.
NEW_USER_ACCOUNT_TYPE = 'new_user'
TODAY = date.today()


# Check if user is logged in.
def is_user_logged_in():
    if session.get("user"):
        return True
    return False


# Gets the user account type to set nav bar and other functions on the page.
def get_user_account_type():
    account = mongo.db.users.find_one({'username': session["user"]}, {'_id': 0, 'account_type': 1})
    account_type = account["account_type"]
    return account_type


# Gets list of all users in the db.
def get_users():
    users = list(mongo.db.users.find().sort("username", 1))
    return users


# Home page
@app.route("/")
@app.route("/home")
def home():
    if is_user_logged_in():
        account_type = get_user_account_type()
    else:
        account_type = NEW_USER_ACCOUNT_TYPE
    return render_template('home.html', account_type=account_type)


# Registration page
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

        # check if passwords match
        password = request.form.get("password")
        confirmPassword = request.form.get("confirm-password")

        if password != confirmPassword:
            flash("Your passwords do not match")
            return redirect(url_for("register"))

        # data being sent to the db
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

        flash("Registration Successful!")
        return redirect(url_for("login"))  # Getting redirected to login here to delay the account type getting requested from the db because it was getting requested to early and threw a NoneType error.

    return render_template("register.html")


# Login page
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
                flash("Welcome, {}".format(request.form.get("username").capitalize()))
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


# Logout button
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Book lesson page
@app.route("/booking/create", methods=["GET", "POST"])
def book_lesson():

     # checks if user is logged in
    if not is_user_logged_in():
        return redirect(url_for("login"))

    # Gets list of users to get the driving instructor select input
    instructors = list(mongo.db.users.find({"account_type": "instructor"}))



    # Booking form data that gets written to db
    if request.method == "POST":
        print(request.form.get("instructor"))
        print(request.form.get("date"))

        if request.form.get('time_slot') is None:
            flash('please choose a time slot')
            return render_template('bookLesson.html', instructors=instructors, account_type=get_user_account_type())
        elif request.form.get("instructor") is None:
            flash('please fill in instructor')
            return render_template('bookLesson.html', instructors=instructors, account_type=get_user_account_type())
        elif request.form.get("date") == '':
            flash('please fill in date')
            return render_template('bookLesson.html', instructors=instructors, account_type=get_user_account_type())

        booking = {
            'instructor': request.form.get("instructor").lower(),
            'student': session['user'],
            'date': request.form.get("date"),
            'time_slot': request.form.get('time_slot'),
            'optional_details': request.form.get('optional_details')
          }
        print(booking)

        mongo.db.bookings.insert_one(booking)
        flash('Booking Succesfull')
    return render_template('bookLesson.html', instructors=instructors, account_type=get_user_account_type())


# This function works out the availabe slots from what slots have already been booked. It gets called from the js file via a fetch call.
@app.route("/get_available_slots")
def get_available_slots():

    # this is the data that is required to find the correct booked slots.
    booking = {
      'date': request.args.get("date", ""),
      "instructor": request.args.get("instructor", "")
    }

    if booking['date'] is None:
        return 'date'

    if booking['instructor'] == '':
        return ''

    available_slots = ALL_SLOTS
    booked_slots = []

    existing_bookings = mongo.db.bookings.find(booking, {"_id": 0, 'time_slot': 1})
    for existing_booking in existing_bookings:
        booked_slots.append(existing_booking['time_slot'])   # querying the db and retreiving what times have been booked for the selected instructor on the selected day.

    if len(booked_slots) < len(available_slots):  # This is removing the booked times from the all times list which will then get sent to Driving lesson times

        available_slots = [item for item in available_slots if item not in booked_slots]

    else:
        flash('Fully Booked')    # if all times are booked it will return fully booked.

    return jsonify({"slots": available_slots})


# View bookings page
@app.route("/bookings")
def view_bookings():
    if not is_user_logged_in():
        return redirect(url_for("login"))

    username = session["user"]
    bookings = list(mongo.db.bookings.find({'student': username}))      # Finds all bookings under the students name

    # Changes the instructors username to there actual name when users view there booked lessons.
    for booking in bookings:  
        instructor = mongo.db.users.find_one({'username': booking["instructor"]}, {'first_name': 1, 'last_name': 1})
        instructor_name = instructor['first_name'] + ' ' + instructor['last_name']
        booking['instructor'] = instructor_name

    return render_template("view_bookings.html", username=username, bookings=bookings, account_type=get_user_account_type())


# booking calender page
@app.route("/booking/calender", methods=["GET", "POST"])
def booking_calender():
    if not is_user_logged_in():
        return redirect(url_for("login"))

    username = session["user"]
    user_account_type = get_user_account_type()
    bookings = []

    # shows all booked lessons for the instructor that is logged in or if an admin is logged in they can see all the bookings.
    if user_account_type == 'admin':
        bookings = list(mongo.db.bookings.find())

    else:
        bookings = list(mongo.db.bookings.find({'instructor': username}))

    return render_template("bookingCalender.html", username=username, bookings=bookings, account_type=get_user_account_type())


@app.route("/booking/<booking_id>/edit", methods=["GET", "POST"])
def edit_booking(booking_id):
    if request.method == "POST":
        current_booking = mongo.db.bookings.find_one(
            {"_id": ObjectId(booking_id)})

        booking = {
            'instructor': current_booking['instructor'],
            'student': current_booking['student'],
            'date': request.form.get("date"),
            'time_slot': request.form.get('time_slot'),
            'optional_details': request.form.get('optional_details')
        }

        mongo.db.bookings.update({"_id": ObjectId(booking_id)}, booking)
        flash("Booking Successfully Updated")
        return redirect(url_for('booking_calender'))

    return redirect(url_for('booking_calender'))



# cancel booking button
@app.route("/booking/<booking_id>/cancel", methods=["GET", "POST"])
def cancel_booking(booking_id):
    if not is_user_logged_in():
        return redirect(url_for("login"))
        account_type = get_user_account_type()

    mongo.db.bookings.delete_one({"_id": ObjectId(booking_id)})
    flash('Booking Canceled!')
    if account_type == "customer":
        return redirect(url_for('view_bookings'))

    return redirect(url_for('booking_calender'))


# User manager page
@app.route("/users/manage", methods=["GET", "POST"])
def user_manager():
    users = get_users()
    return render_template("userManager.html", users=users, account_type=get_user_account_type())


# Edit user form
@app.route("/user/<user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    if request.method == "POST":
   
        # Finds which user there edditing
        current_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # The eddited data
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
        return redirect(url_for("user_manager"))

    return redirect(url_for("user_manager"))

# user search function
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    users = list(mongo.db.users.find({"$text": {"$search": query}}))
    return render_template("userManager.html", users=users, account_type=get_user_account_type())

# booking search function
@app.route("/booking/search", methods=["GET", "POST"])
def search_booking():
    username = session['user']
    user_account_type = mongo.db.users.find_one({"username": username})["account_type"]
    query = request.form.get("query")
    # returns booking calaender so same checks about which instructor, or if an admin is logged in are made
    if user_account_type == 'admin':
        bookings = list(mongo.db.bookings.find({"$text": {"$search": query}}).sort('date'))
    else:
        bookings = list(mongo.db.bookings.find({"$text": {"$search": query}, 'instructor': username}))

    return render_template("bookingCalender.html", bookings=bookings, account_type=get_user_account_type())



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")),
    debug=True)