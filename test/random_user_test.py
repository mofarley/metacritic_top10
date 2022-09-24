import os
import pandas as pd
from sqlite3 import connect
import torch
from natsort import natsorted
import timeit
from helpers_v3 import add_user, find_user_id, score_conv, score, ranking_dict, critic_favorites

path = os.path.dirname(os.path.realpath('metacritic_top10'))

def user_test():

    conn = connect(os.path.join(path, "test/TopTen1.db"))

    titles = pd.read_sql('SELECT * FROM films', conn)

    ranking_filmIDS = pd.read_sql('SELECT film_id FROM rankings', conn)

    conn.close()

    filmID_list = ranking_filmIDS['film_id'].unique().tolist()
    film_names_list = natsorted(titles['title'].unique().tolist())
    #film_names_list = natsorted(film_names)
    for x in film_names_list:
        if 'AND' in x:
            film_names_list.remove(x)
        elif x[-1] == ' ':
            film_names_list.remove(x)
        else:
            continue
            

    temp_dict = {}

    ran = torch.randint(1, 2600, (10,))

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
rankings_copy = rankings.copy()
scores = score_conv(rankings_copy)
critic_score = score(user_id, scores)
'''print(random_user)
print('score:')
print(critic_score)
critic_matches = cosine_similarity(user_id, ranking_old)
print('\ncosine:')
print(critic_matches'''
critic_movie_list = critic_favorites(critic_score)
critic_dict = ranking_dict(rankings, critic_score)

#example of printing out critic, movies, & movies with rankings

'''for m in critic_movie_list[x]:
        if m in critic_dict[x].keys():
            print('{m}: {b}'.format(m=m, b=critic_dict[x][m]))
        else:
            print(m)'''
print(rankings)