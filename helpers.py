import os
from audioop import reverse
from numpy import NaN
import pandas as pd
from sqlite3 import connect
import torch

path = os.path.dirname(os.path.realpath('metacritic_top10'))

def find_user_id():

    conn = connect(os.path.join(path, "TopTen.db"))
    
    critics = pd.read_sql('SELECT id FROM critics', conn)
    #sql to panda
    conn.close()

    user_id = len(critics['id']) + 1
    #in reference to converted sql to pd db, the user id is appended to the end. Therefore, look at the last id index. 
    return(user_id)

#ranking_database returns matrix without scoring implementation (just rankings)

def add_user(user_dict, user_id):
    #this creates user ranking db and appends it to the end of general critic database. 
    conn = connect(os.path.join(path, "TopTen.db"))

    rankings = pd.read_sql('SELECT * FROM rankings', conn)

    titles = pd.read_sql('SELECT * FROM films', conn)

    conn.close()

    film_ids = rankings['film_id'].unique().tolist()
    #convert to list for use as pd dataframe index
    
    user_df_init = pd.DataFrame({'ranking': 0}, index=film_ids)
    #initialize df with row values equaling rankings for each film id for user only 
    
    user_df_init = user_df_init.fillna(0)
    #if user hasn't ranked film - fill as 0
    user_Title_list = list(user_dict.values())
    ''' make sure after title_to_id that dict order stays consistent '''
    user_ID_list = []
    for a in user_Title_list:
        title_to_id = titles[titles['title'] == a]
        user_ID_list.append(int(title_to_id['id']))

    user_isin_films = titles["title"].isin(user_Title_list)
    #isin returns T/F for values passed to it --> if a row has passed value (i.e its in user_dict), it returns true. 
    #Returns entire db of T/F
    
    user_films = titles[user_isin_films]
    #runs T/F output against titles database and returns dataframe of (only) items that are True. 

    rankings_temp = rankings['film_id'].isin(user_Title_list)

    final_rankings = rankings[rankings_temp]
    
    user_df = pd.DataFrame({'film_id' : user_ID_list,
    'critic_id' : NaN, 'ranking' : user_dict.keys()})
    
    #temp fill NaN for critic_id bc want to fill that value with the user id 
    
    user_df['critic_id'] = user_id

    rankings_final = pd.concat([rankings, user_df])

    rankings_matrix = rankings_final.pivot_table(index='film_id',columns='critic_id',values='ranking')

    rankings_matrix = rankings_matrix.fillna(0)

    
    #print(rankings_matrix.loc[67:100, 605])
    #                         row     column



    matrix_final = rankings_matrix.loc[user_ID_list, :]


    #appends user ranking to the end of general critic rankings'''
    return matrix_final


def score_conv(matrix_final):
    for i in range(len(matrix_final)):
        for x in range(len(matrix_final.columns)):
            if matrix_final.iloc[i, x] == 0:
                matrix_final.iloc[i, x] = -8
            else:
                matrix_final.iloc[i, x] = abs(matrix_final.iloc[i, x] - 11)
    return matrix_final


def score(user_id, rankings_pd, k=10):
    temp_dict = {}
    user = torch.tensor(rankings_pd[user_id].values)
    for i in range(1, len(rankings_pd.columns) + 1):
        if i == user_id:
            continue
            #skip user cosine similarity calc
        critic = torch.tensor(rankings_pd[i].values)
        output = sum(user * critic)
        output = (output + 440) / 990
        temp_dict.update({i: output.item()})
    output_dict = dict(sorted(temp_dict.items(), key=lambda item: item[1], reverse=True))
    output_ids = list(output_dict.keys())[:k]
    #final output of k amount of critic scores
    output_scores = list(output_dict.values())[:k]

    output_list = [output_ids, output_scores]
    
    return output_list

#match_list = top scoring critics   &   matrix = ranking matrix 
def ranking_dict(matrix, match_list):
    conv_dict = {1:'1st', 2:'2nd', 3:'3rd', 4:'4th', 5:'5th', 6:'6th', 7:'7th', 8:'8th', 9:'9th', 10:'10th'}
    conn = connect(os.path.join(path, "TopTen.db"))
    critics = pd.read_sql('SELECT * FROM critics', conn)
    films = pd.read_sql('SELECT * FROM films', conn)
    conn.close()
    rank_dict = {}
    for n in match_list[0]:
        temp_rank_dict = {}
        rankings = matrix[n]
        for x in range(10):
            if rankings.iat[x] == 0:
                continue
            else:
                film_name = films.loc[films['id'] == rankings.index[x], ['title']]
                film_name = film_name.iat[0,0]
                temp_dict = {film_name: conv_dict[rankings.iat[x]]}
                temp_rank_dict.update(temp_dict)
                #rank dict is {critic: {film:rank, ...}, 
        get_name = critics.loc[critics['id'] == n, ['critic_name']]
        critic_name = get_name.iat[0, 0]
        critic_rank_dict = dict(sorted(temp_rank_dict.items(), key=lambda item: item[1]))
        rank_dict.update({critic_name: critic_rank_dict})
    return rank_dict
        

def critic_favorites(critic_matches): #critic_matches == output_list from scoring
    dict_critic_favs = {}
    conn = connect(os.path.join(path, "TopTen.db"))
    for critic in critic_matches[0]:
        critic_names = pd.read_sql('SELECT critic_name FROM critics WHERE id == {critic};'.format(critic = critic), conn)
        critic_names = critic_names.iat[0,0]
        critic_favs_db = pd.read_sql('SELECT title FROM films WHERE id IN (SELECT film_id FROM rankings WHERE critic_id == {critic});'.format(critic = critic), conn)
        critic_favs = critic_favs_db['title'].tolist()
        dict_critic_favs.update({critic_names: critic_favs})
    conn.close()
    return(dict_critic_favs)


#potential TODO: add new score to display -> add critic scores by 440 (-440 is minimum score) and divide by 990 (abs[-440] + max=550). 