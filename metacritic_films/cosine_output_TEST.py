import pandas as pd
from sqlite3 import connect
import torch
from helpers import add_user, cosine_similarity, find_user_id

def user_test():

    conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')

    titles = pd.read_sql('SELECT * FROM films', conn)

    ranking_filmIDS = pd.read_sql('SELECT film_id FROM rankings', conn)

    conn.close()

    filmID_list = ranking_filmIDS['film_id'].unique().tolist()

    user_film_randomizer = set()

    temp_dict = {}

    ran = torch.randint(1, 2045, (5,))

    rand_list = []

    for n in ran:
        rand_list.append(filmID_list[int(n)])

    for x in rand_list:
        user_film_randomizer.add(int(x))

    count = 1
    for a in user_film_randomizer:
        temp_dict.update({count: titles.at[a, 'title']})
        count += 1
    print("\n")
    print(user_film_randomizer)

    return temp_dict

user_id = find_user_id()
rankings = add_user(user_test(), user_id)
critic_matches = cosine_similarity(user_id, rankings)



#len == 2044
print(critic_matches)

# skip zero values 