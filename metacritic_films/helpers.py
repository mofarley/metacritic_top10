from audioop import reverse
from numpy import NaN
import pandas as pd
from sqlite3 import connect
import torch

def find_user_id():

    conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/TopTen.db')
    
    critics = pd.read_sql('SELECT id FROM critics', conn)
    #sql to panda
    conn.close()

    user_id = len(critics['id']) + 1
    #in reference to converted sql to pd db, the user id is appended to the end. Therefore, look at the last id index. 
    return(user_id)

# I THINK THIS IS WHERE I SHOULD IMPLEMENT ZERO SKIP. 
def add_user(user_dict, user_id):
    #this creates user ranking db and appends it to the end of general critic database. 
    conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/TopTen.db')

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


def cosine_similarity(user_id, rankings_pd, k=5):
    #rankings_pd 
    
    cosine_dict = {}
   
    #{critic_id: cosine similarity score}
    #users = rankings_pd['critic_id'].unique().tolist()

    #films = rankings_pd['film_id'].unique().tolist()
    

    cos0 = torch.nn.CosineSimilarity(dim=0)
    #https://pytorch.org/docs/stable/generated/torch.nn.CosineSimilarity.html
    
    user = torch.tensor(rankings_pd[user_id].values)
    # seems indexing (ex. rankings_matrix[5]) works along columns. a column shows all films for indexed critic
    
    for i in range(1, len(rankings_pd.columns) + 1):
        #cosine similarity calc for each critic
        if i == user_id:
            continue
        #skip user cosine similarity calc
        critic = torch.tensor(rankings_pd[i].values)
        #see tensor image in readme section
        output = cos0(user, critic)
        cosine_dict.update({i: output.item()})
        #append critic_id:cosine_similarity
    output_dict = dict(sorted(cosine_dict.items(), key=lambda item: item[1], reverse=True))
    #sorts by cosine_value (low to high) --> need to take some time to really understand lamba fx's
    output_ids = list(output_dict.keys())[:k]
    #final output of k amount of critic scores
    output_scores = list(output_dict.values())[:k]

    output_list = [output_ids, output_scores]
    
    return output_list

def critic_favorites(critic_matches): #critic_matches == output_list from cosine_similarity
    list_critic_favs = []
    conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/TopTen.db')
    for critic in critic_matches[0]:
        critic_favs_db = pd.read_sql('SELECT title FROM films WHERE id IN (SELECT film_id FROM rankings WHERE critic_id == {critic});'.format(critic = critic), conn)
        critic_favs = critic_favs_db['title'].tolist()
        list_critic_favs.append(critic_favs)
    conn.close()
    return(list_critic_favs)