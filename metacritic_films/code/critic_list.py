from bs4 import BeautifulSoup
import pandas as pd
from sqlite3 import connect

def list_critics():
    
    conn = connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')
    
    critics = pd.read_sql('SELECT critic_name FROM critics', conn)

    conn.close()

    critic_list = critics['critic_name'].tolist()

    return critic_list
