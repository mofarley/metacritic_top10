import csv
import sqlite3
rankings_list = []
film_set = set()
critic_set = set()
film_rank = ['First','Second','Third','Fourth','Fifth','Sixth','Seventh','Eigth','Ninth','Tenth']
for release_year in range(2015, 2022):
  with open('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/top_ten_csv/{year}.csv'.format(year = release_year), 'r') as f:
      reader = csv.DictReader(f)
      for row in reader:
        critic_set.add((row['Critic/Publisher'],))
  with open('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/unique_films/{year}unique.csv'.format(year = release_year), 'r') as f:
      reader = csv.reader(f)
      for row in reader:
          for value in row:
              film_set.add((value,))
with sqlite3.connect('/Users/mosesfarley/metacritic_top10/metacritic_films/TopTen.db') as c:
  TopTen = c.cursor()
  #for film in film_set:
  TopTen.executemany('INSERT INTO films(title) VALUES (?);', film_set)
  #for critic in critic_set:
  TopTen.executemany('INSERT INTO critics(critic_name) VALUES (?);', critic_set)
  for release_year in range(2015, 2022):
    with open('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/top_ten_csv/{year}.csv'.format(year = release_year), 'r') as a:
      reader1 = csv.DictReader(a)
      for row in reader1:
        critic = row['Critic/Publisher']
        TopTen.execute('SELECT id FROM critics WHERE critic_name = ?', (critic, ))
        critic_temp = TopTen.fetchone()
        critic_id = critic_temp[0]
        number_rank = 1
        for i in film_rank:
          rank = row[i]
          TopTen.execute('SELECT id FROM films WHERE title = ?', (rank, ))
          film_temp = TopTen.fetchone()
          try:
            film_id = film_temp[0]
          except TypeError:
            film_id = 0
          rankings_list.append((film_id, critic_id, number_rank))
          number_rank += 1
  TopTen.executemany('INSERT INTO rankings VALUES (?, ?, ?)', rankings_list)
  c.commit()