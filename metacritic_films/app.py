import os
import sqlite3
from sqlite3 import connect
from flask import Flask, flash, redirect, render_template, request
import pandas as pd
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
    titles = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')
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
        #dict of user film rankings 
        
        user_id = find_user_id()
        rankings = add_user(user_favs, user_id)
        critic_matches = cosine_similarity(user_id, rankings)
        #for above 3: see helper.py
        
        critics = pd.read_sql('SELECT * FROM critics', titles)

        match_filter = critics['id'].isin(critic_matches[0])
        #basic description of how panda filtering works in helpers.py
        
        output = critics[match_filter]

        output = output['critic_name'].tolist()

        num_critics = int(len(output))

        scores = critic_matches[1]
        #increment this in a new column
        return render_template("user_films.html", user_favs=output, scores=scores, length=num_critics)
   
    else:

        movies = pd.read_sql('SELECT * FROM films', titles)

        ranking_filmIDS = pd.read_sql('SELECT film_id FROM rankings', titles)

        titles.close()

        filmID_list = ranking_filmIDS['film_id'].unique().tolist()

        goof =  movies['id'].isin(filmID_list)

        movies = movies[goof]

        film_list = movies['title'].unique().tolist()

        print(len(film_list))

        return render_template("home.html", film_list=film_list)

        #TO DO
        # 1.DONE write descriptions for helper functions 
        # 2.DONE user_films.html: show cosine scores next to critic names. DONE --> down the road graphic display of calculation? 
        # 3. user_films.html: provide links on critic names to list of their favorite films
        # 4. think about changing input layout on home.html... make ranking of favorite films an option?
        # 5. Grindy but... add top 10's for 2011 to 2014
        # ROUGH IDEAS
        # 6. import letterboxd lists???
        # 7. Add film recs based on critic recs (see "collaborative filtering recommendation engine for Anime")
