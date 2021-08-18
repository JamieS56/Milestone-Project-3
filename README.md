# Driving Lesson Booking

The goal of DLB is to make the act of booking a driving lesson as quick and simple for everyone involved and provide a diary of all booked lessons for students and instructors.

## User Stories
### Instrucor Goals:
 
* As an instructor I want to be able to look up and easily view what lessons I have and when.
* I want to know how to contact my students incase of any changes in bookings.
* I want to be able to delete bookings and personalize my available time slots.


### Customer Goals:

* I want to be able to easily book a lesson.
* I want to be able to see what Lessons I have booked.


### My Goals

* An application where you can easily manage the users on it.
* A good looking app that looks nice on both desktop and mobile.


## Design

* Color scheme:
    The three colors I'm going to use are red, white and grey as these are the colors on 'L plates' that learner drivers have and grey is a professional looking color for the nav bar and footer and works nicely with the red and white.

* Typography:
     

* Images:
    I'm gunna put a hero image of a learner driver and there ar n the home page to instantley show visiting users what this website is about.
    plus I will have the logo at the top of the nav bar on each page.

## Wireframes


## Features

* Responsive on all devices
* Nav bar that is a hidden side nav on mobile
* Create account and login validation
* Able to edit user profiles(excluding passwords)
* Able to delete and edit bookings
* have different access levels based on account type.
* Search booking and user features.


## Technologies Used

### Languages Used

* HTML
* CSS
* JavaScript
* Python

### Frameworks, Libraries and Programs Used:

1. Flask
    * Flask is the framework I used to create my app it depends on the Jinja template engine and the Werkzeug WSGI toolkit.
2. Materialize
    * Materialize was used to help make the website responsive and implement features like select forms and date pickers.
3. jQuery
    * I used this in my js files mainly to help initialize materialize js features.
4. Font Awesome
    * I used Font Awesome to provide icons for my app.
5. Google Fonts
    * I used google fonts to provide the wonts for my app.
6. Mongo DB
    * The database system i'm using to store all user data and bookings.
7. PyMongo
    * Pymongo was used to help interact with MongoDB through python.
8. Git
    * Used to push all code to github from git pod workspace
9. GitHub
    * Used to store all the code after pushing from git
10. Heroku
    * Used to deploy application to the web.
11. Balsamiq
    * Used to create Wireframes


## Testing

### Instructor Goals Testing:
1. "As an instructor I want to be able to look up and easily view what lessons I have and when."

    All this will be available within the Booking Calender Page which will show all lessons that the instructor has and can search by date and by student. for convinience the lessons will appear in date order so the instructor can see there next lesson.

2. "I want to know how to contact my students incase of any changes in bookings."

    On the booking calender page it will show the student and there contact info on the booking card so the instructor can contact them.

3. "I want to be able to delete bookings and personalize my available time slots."

    The ability for both instructors and students to cancel booked lessons is there even with a confirmation popup to avoid mistakes. The ability to personalise time slots though is not yet implemented and for more information please look at the future scope section.


### Student Goals Testing:

1. "I want to be able to easily book a lesson."

    As soon as you make an account it takes you to the home screen which propmts you to book a lesson also it is the second tab in the side bar after home encouraging the useer to book a lesson. once they click on it the user ony has to input 3 fields: driving instructor, date, time and an optional 4th of any other information the instructor may need like a pickup location.

2. "I want to be able to see what lessons I have booked."

    The "My Bookings" page clearly shows all bookings and information about the booking to the user, and can be searched by student, instructor or date.



### My Goals Testing:
1. "An application where you can easily manage the users on it."
    I have a fully fonctioning user manager page where admins can search through the database of users and edit their profiles, excluding passwords, if needed and change account types. For easy use there is a search feature where you can search users by first name, last name and username.

2. "A good looking app that looks nice on both desktop and mobile."

    With the help of materialize the app looks sleek on desktop, tablet and mobile. I have fully used there grid system throughout development to create a responsive layout.
    I also have used a materialize stepper which was created by [Floris List](https://codepen.io/flist) which I found on [code pen](https://codepen.io/flist/pen/mqXemY). It works great for what I needed which was a simple form layout which looks great on all screen sizes and keeps you on the same page throughout the whole booking proccess. Originally I had split the booking across two pages so I could load the timeslots with a new page but because of the fetch function I could load in the data without refreshing the page.


### Other teting:

* Testing sidenav:

    The sidenav that is used so mobile users can access the menu wasn't working. This was because jquery wasn't connected so added it to the base html and works now.

* Passing data using fetch:

    I started off using session to store data and make it available on the html page. Now I am calling the python function via a js fetch call. I had a problem where the call was returning the event data and not the time slot data I wanted so using the .json() functionImanaged to extract the correct data and injected it into my select input as options using .innerHTML.

``` javascript  
    async function getAvailableSlots(_eventdata, instructor = $("#instructor-selector").val(), date = $('#lesson-booking-date-picker').val()) {

        response = await fetch(`/get_available_slots?date=${date}&instructor=${instructor}`)
        response.json().then(data => {
            slots = data.slots
            let timeSlotsHTML = `<option value="" disabled selected>Choose Time Slot</option>`;
            for (slot in slots) {
                timeSlotsHTML += `<option value="${slots[slot]}">${slots[slot]}</option>`
            }
            document.getElementById('time-selector').innerHTML = timeSlotsHTML;
        })
    }
```

* NoneType error thrown after creating an account:

    When an account is created it writes the accoun_type to the db but it didn't write it quick enough and it was getting looked up when `get_account_type()` is called when rendering the home page. To get around this I render the login page making the user login again which gives enough time for the account to be written to the db and then be called after the user has logged in.

### Testing web page

#### Nav Bar and Links

    All links in the footer redirect to the correct website on a new tab for the user to view our socials. all links within the website linking with other pages all work correctly and consistently plus correct links show up in the nav bar for who is logged in and there account type. They also all work correct;y on mobile and because of the hidden side nav are easily accessibly and look good.

#### Booking Lessons

    The booking lessons form works well all data is successfully written to the data base and if any of the required fields aren't filled in it will flash a message on screen and not write any data to the database. I would have used the required attribute like in the registration and login form but for some reason it didn't work probbably to do fith the code for the stepper but i'm not sure what part so this was my solution.

#### Viewing bookings

    Viewing bookings works well, you can only see the bookings you've booked and no one elses it looks neat and clean and you can cancel a booking if you want to and even has a warning popup to avoid unwanted cancelations.

#### Booking callender

    The booking callender works well, the instructor can view all lessons that are booked to them, can cancel lessons, edit bookings and can even search through them by name and date.

#### User Manager

#### Create account/ Login

#### Responsive design



## Deployment

This is how I deployed my project to Github and Heroku

1. First of all I created a github repository using Code institutes github-full-template on git pod.

2. I then created my base files and installed required packages that I needed such as flask. 

3. One of these files was the env.py file which has sensitive data that I didn't want uploaded to git such as my mongo db login and secret key. so I created a .gitignore file and put the env.py file and pycache in so they didn't get uploaded to github.

4. I then wrote in the terminal `git add -a`, `git commit` and then `git push` to push it to my github repository

5.  Next in the terminal I created requirements.txt by typing `pip3 freeze --local > requirements.txt` this tells heroku which apps and dependencies are needed to run the app.

6. Then I created a procfile by typing `echo web: python app.py > Procfile` into the terminal, this tells heroku which file runs the app. I then pushed to github again.

7. I then went to [Heroku.com](https://dashboard.heroku.com/apps) logged in and clicked new and then create a new app.

8. I then named my app with a unique name and selected Europe as my region then created app.

9. I then went to the deploy tab of my app then selected connect to GitHub, I entered the git hub repository name and then search and clicked on my app.

10. Then I clicked on settings selected reveal config variables and inputted all the variables I have in my env.py file.

11. Then back on the deploy tab I clicked enable automatic deployment and then hit deploy branch. You know it's worked when it says "Your App was successfully deployed.".

12. Now it automatically updates when we push to github.



### Note:

At the start of my project I was pushing straight to Heroku using the cli commands 

```
    $ git add .
    $ git commit -am "make it better"
    $ git push heroku master
```

This meant that I was not saving to github and not saving my commit messages either. When I realised this I switched back to the way I layed out above. I realised this when git pod went down and I lost my workspace and nothing I had done since the initial commit was saved to github. luckily I managed to clone the repository using 
`heroku git:clone -a myapp` command and didn't loose much work





## Photos links

* Hero Image used on the home page was from [unionschoolofmotoring](https://www.unionschoolofmotoring.co.uk/wp-content/uploads/2020/10/prices-car.png.webp)

* The L plate used in the nav bar was taken from [passmefast](https://blog.passmefast.co.uk/images/l-plate-300x300.png)


## Code links

* The Stepper I used in my booking form was created by [Floris List](https://codepen.io/flist/pens/) on [codepen](https://codepen.io/flist/pen/mqXemY) It came with prewritten html, js and css files that I have adapted for my needs.

* I have used lots of official documentation and websites to help me through out my project:
    * [w3schools](https://www.w3schools.com/) - I used to help me for using Python to interact with mongo db
    * [Mozilla](https://developer.mozilla.org/en-US/docs/Web) - I used this for helping me with the code that fetches the available time slots and also selecting elements with 'disabled' attributes.
    * [MongoDB docs](https://docs.mongodb.com/) - Just generaly setting up my data base and also accessing it through my app.
    * [Flask](https://flask.palletsprojects.com/en/2.0.x/) - If I had anything that I was stuck on in my app.py file I usually reffered to this.
    * [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) - I used Jinja docs to help set up templates and more speciffically filtering within the templates.
    * [Materialize](https://materializecss.com/) - Materialize was what I used to style the whole app so if I had any problems styling I used there official docs.
