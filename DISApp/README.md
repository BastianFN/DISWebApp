# Introduction
This project is a website running Python and Flask library.
The schema of the database is a ufo forum, where people can post about sightings and add to the sightings table, which can be viewed in a heatmap of ufo sightings. Note that in order to see all features, you will need access to the internet.



## Requirements:
Run the code below to install the necessary modules.

>$ pip install -r requirements.txt

If for some reason you get a pb_config error, change psycopg2 to psycopg2-binary in requirements.txt and run the
command again.


## Database init
1. Change the database variable db in __init__.py, create_database.py and models.py to your own database.
2. Run the create_database.py file in the DISapp folder. This will create the database and the tables.


## Running flask
Run the run.py file in the DISapp folder. The website should now run on localhost:5000, taking you to the front page.


## Blast Off with the Website 🚀
Y'all ready for this? Fire up your engines by running run.py and it'll jet you off to a web app in another galaxy at localhost:5000. 🌌

Now that you've docked at the homepage, there's a secret mission waiting for you. Hunt down the hidden button, which whispers "It's uffo time". Give it a gentle nudge, and whoosh you'll time-warp to a heatmap filled with UFO sightings! 🛸

Or, if you like shortcuts, be a warp-speed wizard and hit the heatmap button right on the top bar. 🧙‍♂️

Feel like sharing your close encounters? Hit the posts button. But wait, you gotta be part of the UFO Hunters' Guild to share your stories. If you're not signed in, you'll be teleported to the login page.🌪️ Don't fret, you can get the UFO Hunters' credentials right here:

username: bastian, password: 1
username: simon, password: 2
username: magnus, password: 3
username: kasper, password: 4
username: dis, password: uffo

Sign in and you’ll be bestowed the power to share your galactic encounters! 🌠 Got a latitude and longitude for your sighting? Bam! It's on the heatmap. 🌍

You can also go interstellar and view posts created by other UFO enthusiasts under post creation. Although you can’t like or comment (alien technology limitations, you know), we've kept buttons as a cryptic message for what the future may bring! 🌟

Strap in, have fun, and remember – The truth is out there! 👽
