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
    I also have used a materialize stepper which was created by [Floris List](https://codepen.io/flist) which I found on [code pen](https://codepen.io/flist/pen/mqXemY). It works great for what I needed which was a simple form layout which looks great on all screen sizes and keeps you on the same page throughout the whole booking proccess. Originally I had split the booking across two pages so i could load the timeslots with a new page but because of the fetch function i could load in the data without refreshing the page.


### Other teting: 
* Testing sidenav
The sidenav that is used so mobile users can access the menu wasn't working. This was because jquery wasn't connected so added it to the base html and works now.

* Passing data using fetch
I started off using session to store data and make it available on the html page. Now I am calling the python function via a js fetch call. I had a problem where the call was returning the event data and not the time slot data I wanted so using the .json() functionImanaged to extract the correct data and injected it into my select input as options using .innerHTML.

`    

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

`

## Deployment
### Notes 
For the first couple of weeks of my projectIdin't realise I was pushong straight to heroku and not to github, which I realised when the gitpod workspaces went down and I lost the work on the workspace and it wasnt on github but was on heroku. so I cloned the heroku repository into a new workspace for my project using 'heroku git:clone -a APP-NAME' and reinstalled the packages that I needed and remade my env file.



Photos links.

https://www.unionschoolofmotoring.co.uk/wp-content/uploads/2020/10/prices-car.png.webp

https://blog.passmefast.co.uk/images/l-plate-300x300.png


code links

https://codepen.io/flist/pen/mqXemY