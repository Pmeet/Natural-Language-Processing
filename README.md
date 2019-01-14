# Natural-Language-Processing
Python app which detects phrases like "remind me to do laundry" and sets a reminder for same in google calendar 

# How to test 
- step 1: download whole repository and extract it
- step 2: delete the token.json file 
- step 3: run the project.py file and it will open your default browser to authenticate your credentials as a google account user
- step 4: sign in and close the browser when you recieve message on screen "Authentication successful"
- step 5: Python interface will open and you can test the application
 
# How it works
There are four main python modules used to carry out the task :

1 Google Calendar API for python
- used to set events for the users and also to get upcoming events of user

2 Google speech recognition module for python
- used to get speech input from user

3 spacy 
- spacy is used to perform nlp on the phrase which was taken as input through speech or text by the interface

4 appJar 
- the interface of the application is developed using this module
