from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, make_response
import pyrebase
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import json
import random

load_dotenv()
app = Flask(__name__)

data = [{'date': "12-2-2004", 'weight': 60, 'blood_pressuer': 30}, {'date': "12-2-2003", 'weight': 20, 'blood_pressuer': 40}, ]

config = {
  "apiKey": os.getenv("API_KEY"),
  "authDomain": os.getenv("AUTH_DOMAIN"),
  "databaseURL": os.getenv("DATABASE_URL"),
  "storageBucket": os.getenv("STORAGE_BUCKET")
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}


#Login
@app.route("/signin")
def login():
    return render_template("login.html", person = person)

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html", person = person)

#Welcome page
@app.route("/")
def index():
    if person["is_logged_in"] == True:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

#Dashboard
@app.route("/dashboard")
def dashboard():
    if person["is_logged_in"] == True:
        return render_template("dashboard.html", person = person, data=data)
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        print(email)
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
    
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
        
            #Redirect to welcome page
            return redirect(url_for('dashboard'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        age = result["age"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            person['age'] = age
            #Append data to the firebase realtime database
            data = {"name": name, "email": email, "age": age}
            db.child("users").child(person["uid"]).set(data)

            #Go to welcome page
            return redirect(url_for('dashboard'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run(debug=True)