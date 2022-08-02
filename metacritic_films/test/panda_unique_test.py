from numpy import NaN
import pandas as pd
from sqlite3 import connect

user_dict = {1: 'Endless Poetry', 2: 'War on Everyone', 3: 'Three', 4:'Blade Runner 2049', 5: 'Mom and Dad'}

conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')

rankings = pd.read_sql('SELECT * FROM rankings', conn)

titles = pd.read_sql('SELECT * FROM films', conn)

critics = pd.read_sql('SELECT * FROM critics', conn)

conn.close()

film_ids = rankings['film_id'].unique().tolist()

user_df_init = pd.DataFrame({'ranking': 0}, index=film_ids)

user_df_init = user_df_init.fillna(0)

test = titles["title"].isin(list(user_dict.values()))

user_films = titles[test]

critic_count = rankings['critic_id'].unique()

user_id = len(critic_count) + 1

user_df = pd.DataFrame({'film_id' : user_films['id'],
'critic_id' : NaN, 'ranking' : user_dict.keys()})

user_df['critic_id'] = user_id

#rankings_final = pd.concat([rankings, user_df])

goo = critics['id'].isin([588, 503, 271, 355, 275])

output = critics[goo]

output = output['critic_name'].tolist()

print(output)
#need to find a way to include rankings

#1. continue with creation of seperate user ranked pd database
# and merge it into the master pd database 

#or
#2. try to append user films to sql database 

# I think 1 is more practical, but will revisit