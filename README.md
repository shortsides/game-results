## Game Results Application (CS50W Capstone Project)

My Game Results app helps friends who play offline games together like board games or casual sport to keep track of the results of their games and see how they stack up against each other with a ranking system.

Users can add their favourite games, update their recent scores and track
how they're doing against other players. There is also an overall ranking, 
which compares all players across all games to see who is the ultimate
game champion!

### How this app meets the project requirements

This app has several features making it more complex than previous projects, including:
 - Implementation of Microsoft Research's TrueSkill Bayesian inference system for the Game Result Application's player rating system. After at least 3 results have been added for a game, the rating system will start to calculate player ratings. This system quantifies players’ skill points using a Bayesian inference algorithm. The more games that are played, the more accurate the rankings become.
 - A JavaScript API handling the form validation for the 'Submit Results' form

This application utilises Django with 4 models on the back-end and JavaScript on the front-end.

All parts of this web application are mobile-responsive.

### Files in project
  - `gameresults` main app directory
    - `static/gameresults` contains all static content
        - `index.js` scripts for the app
        - `styles.css` contains styling for app
        - `node_modules/select-pure` contains the installed select-pure library (see Citations)
    - `static/images/favicon.ico` favicon for app
    - `templates/gameresults` contains all app templates
        - `change_password.html` password change page
        - `games.html` the page to view and add games to the database
        - `index.html` app homepage with the Submit Result feature and a feed of Recent Results
        - `layout.html` main layout of app, include navbar
        - `login.html` user login page
        - `rankings.html` page where users can view rankings for games
        - `register.html` user registration page
    - `admin.py` registers the models for the admin page
    - `apps.py` registers the gameresults app
    - `helpers.py` contains the code for the calculate rankings function
    - `models.py` models for the app
    - `urls.py` app URLs
    - `views.py` app views
  - `NScrewgameresults` project directory
    - `asgi.py` ASGI config
    - `settings.py` django app settings
    - `urls.py` registered project URLs
    - `wsgi.py` WSGI config
  - `manage.py` project run file
  - `requirements.txt` project installation requirements

### How to install and run the application
 - Install the dependencies outlined in requirements.txt with the command `pip install -r requirements.txt`
 - Navigate to the root folder and use the commands `python manage.py makemigrations` and `python manage.py migrate` to set up the SQlite database
 - Run the application with python manage.py runserver

### Citations
Select Pure https://github.com/dudyn5ky1/select-pure (used for the nice drop-down menus that help with selection of data for the Submit Results form).
TrueSkill https://github.com/sublee/trueskill (used for the player rating calculation)
