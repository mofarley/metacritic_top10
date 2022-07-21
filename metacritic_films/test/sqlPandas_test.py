import pandas as pd
from sqlite3 import connect

import 


conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')

rankings = pd.read_sql('SELECT * FROM rankings', conn)

users = rankings['critic_id'].unique().tolist()

films = rankings['film_id'].unique().tolist()

rankings_matrix = rankings.pivot_table(index='critic_id',columns='film_id',values='ranking')

rankings_matrix = rankings_matrix.fillna(0)

print(rankings_matrix.head())