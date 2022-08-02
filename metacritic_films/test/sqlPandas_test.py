import pandas as pd
from sqlite3 import connect

import torch


conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')

rankings = pd.read_sql('SELECT * FROM rankings', conn)

users = rankings['critic_id'].unique().tolist()

films = rankings['film_id'].unique().tolist()

rankings_matrix = rankings.pivot_table(index='film_id',columns='critic_id',values='ranking')

rankings_matrix = rankings_matrix.fillna(0)

def similar_users(user_id, matrix, k=5):
    cosine_list = []
    # ^ list of lists containing [critic_id, cosine similarity score]
    cos0 = torch.nn.CosineSimilarity(dim=0)
    user = torch.tensor(matrix[user_id].values)
    # seems indexing (ex. matrix[5]) works along columns. a column shows all films for indexed critic
    for i in range(1, len(matrix.columns) + 1):
        if i == user_id:
            continue
        critic = torch.tensor(matrix[i].values)
        output = cos0(user, critic)
        cosine_list.append([i, output.item()])

    #test_critic = torch.tensor(matrix[11].values)
    
    return cosine_list


print(len(films))