from bs4 import BeautifulSoup
import csv
with open("metacritic_films\sources\Film Critic Top 10 Lists - Best Movies of 2021 - Metacritic.html", "r") as f:
    topten = BeautifulSoup(f, "html.parser")

table = topten.find("table")
output_rows = []
for critics in table.find_all("tr"): 
    films = critics.find_all("td")
    output_row = []
    critic = critics.find_all("th")
    for name in critic:
        name = name.text
        name = name.replace("View full list", "")
        output_row.append(name)
    for film in films:
        output_row.append(film.text)
    output_rows.append(output_row)
#output_row = output_row[0].split("\n")
print(output_rows)