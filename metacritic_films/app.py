import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request

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
        user_favs = [film1, film2, film3, film4, film5, film6, film7, film8, film9, film10]
        return render_template("user_films.html", user_favs=user_favs)
    else:
        film_list = set()
        db = sqlite3.connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')
        TopTen = db.cursor()
        TopTen.execute('SELECT title FROM films')
        x = TopTen.fetchall()
        for i in x:
            film_list.add(i[0])
        db.close()
        return render_template("home.html", film_list=film_list)