import os
import sqlite3
from sqlite3 import connect
from flask import Flask, flash, redirect, render_template, request
import pandas as pd
import torch
from helpers import add_user, cosine_similarity, find_user_id

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


def apology(code=400):
    """Render message as an apology to user."""
    return render_template("apology.html"), code

@app.route("/", methods=["GET", "POST"])
def home():
    #film_selection = db.cursor()
    #To Do --> going to text a full text search
    if request.method == "POST":
        film1 = request.form.get("film_one")
        film2 = request.form.get("film_two")
        film3 = request.form.get("film_three")
        film4 = request.form.get("film_four")
        film5 = request.form.get("film_five")
        film6 = request.form.get("film_six")
        film7 = request.form.get("film_seven")
        film8 = request.form.get("film_eight")
        film9 = request.form.get("film_nine")
        film10 = request.form.get("film_ten")
        
        user_favs = {1:film1, 2:film2, 3:film3, 4:film4, 5:film5, 6:film6, 7:film7, 8:film8, 9:film9, 10:film10}

        return render_template("user_films.html", user_favs=user_favs)
    else:
        titles = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')

        movies = pd.read_sql('SELECT title FROM films', titles)

        film_list = movies['title'].unique().tolist()

        titles.close()

        return render_template("home.html", film_list=film_list)

        #To Do --> Finish flask work(figure out redirect and render_template stuff)