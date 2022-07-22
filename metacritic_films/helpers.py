from numpy import NaN
import pandas as pd
from sqlite3 import connect
import torch

def find_user_id():
    
    conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')

    critics = pd.read_sql('SELECT id FROM critics', conn)

    conn.close()

    user_id = len(critics['id'] + 1)

    return(user_id)


def add_user(user_dict, user_id):

    conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')

    rankings = pd.read_sql('SELECT * FROM rankings', conn)

    titles = pd.read_sql('SELECT * FROM films', conn)

    conn.close()

    film_ids = rankings['film_id'].unique().tolist()

    user_df_init = pd.DataFrame({'ranking': 0}, index=film_ids)

    user_df_init = user_df_init.fillna(0)

    test = titles["title"].isin(list(user_dict.values()))

    user_films = titles[test]

    user_df = pd.DataFrame({'film_id' : user_films['id'],
    'critic_id' : NaN, 'ranking' : user_dict.keys()})

    user_df['critic_id'] = user_id

    rankings_final = pd.concat([rankings, user_df])

    return rankings_final


def cosine_similarity(user_id, rankings_pd, k=5):
    cosine_list = []
    # ^ list of lists containing [critic_id, cosine similarity score]
    users = rankings_pd['critic_id'].unique().tolist()

    films = rankings_pd['film_id'].unique().tolist()
    
    rankings_matrix = rankings_pd.pivot_table(index='film_id',columns='critic_id',values='ranking')

    rankings_matrix = rankings_matrix.fillna(0)

    cos0 = torch.nn.CosineSimilarity(dim=0)

    user = torch.tensor(rankings_matrix[user_id].values)
    # seems indexing (ex. matrix[5]) works along columns. a column shows all films for indexed critic
    
    for i in range(1, len(rankings_matrix.columns) + 1):
        if i == user_id:
            continue
        critic = torch.tensor(rankings_matrix[i].values)
        output = cos0(user, critic)
        cosine_list.append([i, output.item()])

    #test_critic = torch.tensor(matrix[11].values)
    
    return cosine_list