from encodings import search_function
import os
import sqlite3
from sqlite3 import connect
from natsort import natsorted
from flask import Flask, render_template, request
import pandas as pd
from helpers import add_user, find_user_id, ranking_dict, score, score_conv, critic_favorites

path = os.path.dirname(os.path.realpath('metacritic_top10'))

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


def apology(code=400):
    """Render message as an apology to user."""
    return render_template("apology.html"), code

def render_home(alert_msg):
        titles = connect(os.path.join(path, "TopTen.db"))

        movies = pd.read_sql('SELECT * FROM films', titles)

        ranking_filmIDS = pd.read_sql('SELECT film_id FROM rankings', titles)

        titles.close()

        filmID_list = ranking_filmIDS['film_id'].unique().tolist()

        movie_filter =  movies['id'].isin(filmID_list)

        movies = movies[movie_filter]

        film_list = natsorted(movies['title'].unique().tolist())

        for x in film_list:
            if 'AND' in x:
                film_list.remove(x)
            elif x[-1] == ' ':
                film_list.remove(x)
            else:
                continue
        
        return render_template("home.html", film_list=film_list, alert_msg=alert_msg)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        titles = connect(os.path.join(path, "TopTen.db"))

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
        
        ranking_str = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        user_favs = {1:film1, 2:film2, 3:film3, 4:film4, 5:film5, 6:film6, 7:film7, 8:film8, 9:film9, 10:film10}
        user_favs_list = list(user_favs.values())
        duplicate_check = set()
        for values in user_favs.values():
            if values == '':
                alert = 1
                return render_home(alert)
            duplicate_check.add(values)
        if len(duplicate_check) < 10:
            alert = 1
            return render_home(alert)
        #dict of user film rankings 
        user_id = find_user_id()

        rankings = add_user(user_favs, user_id)
        #return matrix of ranks with rows = films ranked by user & columns = every critic

        rankings_copy = rankings.copy()

        scores = score_conv(rankings_copy)
        #convert rankings matrix (see above 'rankings) to score matrix
        
        critic_matches = score(user_id, scores)
        #returns 10 critics with highest total scores
        #for above 3: see helper.py

        
        critics = pd.read_sql('SELECT * FROM critics', titles)

        titles.close()

        match_filter = critics['id'].isin(critic_matches[0])
        #basic description of how panda filtering works in helpers.py
        
        critic_match_list = critics[match_filter]

        critic_match_list = critic_match_list['critic_name'].tolist()

        rt_search_list = []

        publisher_csv = pd.read_csv(os.path.join(path, "databases/publishers.csv"))
        publisher_list1 = publisher_csv.values.tolist()
        publisher_list = []
        for p in publisher_list1:
            publisher_list.append(p[0])

        critic_match_allmovies = critic_favorites(critic_matches)
        #dict = {matched critic: [every movie they've ranked], ...}

        critic_fav_dict = ranking_dict(rankings, critic_matches)

        for name in critic_fav_dict:
            #if name is publisher: dont search rottentomatoes
            if name in publisher_list:
                publisher = name.replace(' ', '+').strip()
                search_name = '{query}+movie+reviews'.format(query=publisher)
                rt_search = 'https://www.google.com/search?q={search_name}'.format(search_name=search_name)
            else:
                search_name = name.replace('.', '').replace(' ', '-').strip()
                rt_search = 'https://www.rottentomatoes.com/critics/{search_name}/movies'.format(search_name = search_name)
            rt_search_list.append(rt_search)


        num_critics = int(len(critic_match_list))
        

        return render_template("user_films.html", critic_movies = critic_match_allmovies, length=num_critics, 
        rt_search = rt_search_list, critic_fav_dict = critic_fav_dict, user_list=user_favs_list)
   
    else:

        return(render_home(alert_msg=''))

        #TO DO
        # 1.DONE write descriptions for helper functions 
        # 2.DONE user_films.html: show cosine scores next to critic names. DONE --> down the road graphic display of calculation? 
        # 3.DONE user_films.html: provide links on critic names to list of their favorite films
        # 4.BACKBURNER think about changing input layout on home.html... make ranking of favorite films an option?
        # 5.DONE Grindy but... add top 10's for 2011 to 2014
        # 6. on user_films.html: add user picks drop down in white space next to Critic Matches header.
        # ROUGH IDEAS
        # 6. import letterboxd lists???
        # 7. Add film recs based on critic recs (see "collaborative filtering recommendation engine for Anime")
