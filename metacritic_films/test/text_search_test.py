import os
import sqlite3

db = sqlite3.connect('/Users/mosesfarley/metacritic_top10/metacritic_films/databases/TopTen.db')
TopTen = db.cursor()
TopTen.execute('SELECT title FROM films')
x = TopTen.fetchall()
for i in x:
    print(i[0])
db.close()