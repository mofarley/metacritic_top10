import pandas as pd
from sqlite3 import connect
import torch
from helpers_v2 import add_user, cosine_similarity, find_user_id

def user_test():

    conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')

    titles = pd.read_sql('SELECT * FROM films', conn)

    ranking_filmIDS = pd.read_sql('SELECT film_id FROM rankings', conn)

    conn.close()

    filmID_list = ranking_filmIDS['film_id'].unique().tolist()

    temp_dict = {}

    ran = torch.randint(1, 2045, (10,))

    rand_list = []

    for n in ran:
        rand_list.append(int(n))


    #the set (user_film_randomizer) will have different order than rand_list
    count = 1
    for a in rand_list:
        goof = titles.loc[titles['id'] == a, ['title']]
        temp_dict.update({count: goof.iat[0,0]})
        count += 1

    return temp_dict

peter_traversID = {1: 67, 2: 86, 3: 88, 4: 112, 5: 168, 6: 196, 7: 222, 8: 301, 9: 325, 10: 333}
peter_travers = {1: 'Dune', 2: 'Dunkirk', 3: 'If Beale Street Could Talk', 4: 'The Tragedy of Macbeth', 
5: 'Fences', 6: 'Minari', 7: 'Sully', 8: 'Belfast', 9: 'Lady Bird', 10: 'Carol'}
user_id = find_user_id()
random_user = user_test()
rankings = add_user(peter_travers, user_id)
critic_matches = cosine_similarity(user_id, rankings)
print(critic_matches)
# skip zero values 