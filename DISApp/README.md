# Introduction
This project is a website running Python and Flask library. It 
The schema of the database is a ufo forum, where people can post about sightings and add the the sightings table, which can be viewed in a heatmap of ufo sightings.



## Requirements:
Run the code below to install the necessary modules.

>$ pip install -r requirements.txt


## Database init
1. set the database variable db in __init__.py file, create_database.py and models.py


## Running flask
Run the run.py file in DISapp folder. The website should now run on localhost:5000, taking you to the front page.



## Using the website

Running run.py run the webapp on localhost:5000. Here pressing the "It's uffo time" will take you to the heatmap of all the ufo sightings. You can also press the posts tab, which will either take you to the login page if you are not logged in, or the posts tab if you are. Using either username: bastian, password: 1, username: simon, password: 2, username: magnus, password: 3, or username: kasper, password: 4 will log you in. Now you can go to the posts tab again and write a comment about the ufo and insert the lattitude and longitude of the sighting. This will now also be in the heatmap. Posts by you and others can be viewed under the post creation. It is not possible to like or comment, but we have added the buttons as an indication of what further development would look like. Our focus has been on the heatmap.
