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
            "accountType": "customer",
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
        session['bookedLessons'] = list(mongo.db.bookings.find({'student': session["user"]},{'_id': 0}))

        return render_template("viewBookings.html", username=username)

    return redirect(url_for("login"))


@app.route("/bookLesson/<username>", methods=["GET", "POST"])
def bookLesson(username):
    # this is a list of the bookable times to the user to compare to what is already booked in the database. in the future it will be able to be set by the instructor and fetched from the database.
    if session["user"]:  # checks if user is logged in
        users = list(mongo.db.users.find())  # Gets list of users to get the driving instructor select input
        if request.method == "POST":
            booking = {  # The dictionary that will be submitted in the final form to the db
                'instructor': request.form.get('instructor'),
                'date': request.form.get('date')}

            session['booking'] = booking

            return redirect(url_for('get_bookableTimes'))

        return render_template('bookLesson.html', users=users)

    return redirect(url_for("login"))


@app.route("/get_bookableTimes")
def get_bookableTimes():

    booking = session.get('booking')
    allTimes = ['10:00-11:00', '11:00-12:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00']
    bookedTimes = []

    for x in mongo.db.bookings.find(booking, {"_id": 0, 'timeSlot': 1}):
        bookedTimes.append(x['timeSlot'])   # querying the db and retreiving what times have been booked for the selected instructor on the selected day.

    if len(bookedTimes) < len(allTimes):  # This is removing the booked times from the all times list which will then get sent to Driving lesson times
        for x in allTimes:
            for y in bookedTimes:
                if x == y:
                    allTimes.remove(x)

        bookableTimes = allTimes

    else:
        bookableTimes = 'Fully Booked'    # if all times are booked it will return fully booked.

    session['bookableTimes'] = bookableTimes
    return redirect(url_for('bookLessonTime'))


@app.route("/bookLesson_time/", methods=["GET", "POST"])  # Book Lesson times route
def bookLessonTime():

    if request.method == "POST":
        booking = {
            'instructor': session['booking']['instructor'],
            'student': session['user'],
            'date': session['booking']['date'],
            'timeSlot': request.form.get('bookingTime')
        }
        mongo.db.bookings.insert_one(booking)
        flash('Booking Succesfull')
        return redirect(url_for('home'))

    return render_template('bookLessonTime.html')


@app.route("/bookingCalender/<username>", methods=["GET", "POST"])
def bookingCalender(username):


    return render_template("bookingCalender.html", username=username)


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


@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if request.method == "POST":
        current_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        submit = {
            "username": request.form.get("username").lower(),
            'password': current_user['password'],
            "firstName": request.form.get("first_name"),
            "lastName": request.form.get("last_name"),
            "phoneNumber": request.form.get("phone-number"),
            "email": request.form.get("email"),
            "accountType": request.form.get("accountType"),
        }
        mongo.db.users.update({"_id": ObjectId(user_id)}, submit)
        flash("User profile Successfully Updated")
        return redirect(url_for("userManager"))

    users = list(mongo.db.users.find().sort("username", 1))
    return render_template("userManager.html", users=users)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")),
    debug=True)
