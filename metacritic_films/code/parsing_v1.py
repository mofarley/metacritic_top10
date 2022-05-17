from bs4 import BeautifulSoup
import csv
with open("metacritic_films/sources/Film Critic Top 10 Lists - Best Movies of 2021 - Metacritic.html", "r") as f:
    topten = BeautifulSoup(f, "html.parser")

tables = topten.find_all("table")
#eventually change tables to find_all. Also remember find_all returns a set.
output_rows = []
#output_rows = final list that's converted to csv
for table in tables:
    critics_and_films = table.find_all("tr") 
    #critics_and_films --> see line 14 on parsing_notes.txt
    count = 0
    critics_and_films_total = len(critics_and_films)
    #critics_and_films_total = # of <tr>'s in a given table
    publisher_name = table.find('caption').text
    output_row = []
    while count < critics_and_films_total:
        for i in range(2):
            output_row.append(critics_and_films[count].text)    
            count += 1
        # if count starts at zero, it ends up at two at the end of the
        # i loop. so if we're look for (example) a [0] and [1] index for critics and films
        # respectively then we subtract count by 2 and 1 to get the desired index values
        critic_index = count - 2
        films_index = count - 1
        critic = output_row[critic_index].replace("View full list", "").strip('\n').rstrip()
        if critic == 'Staff consensus':
            output_row[critic_index] = publisher_name.strip()
        else:
            output_row[critic_index] = critic
        films = output_row[films_index].strip('\n').split('\n')
        output_row[films_index] = films
        #USE A DICTIONARY!! --> make this iterative since
        # more than two <tr>'s in certain tables
        fav_films = {output_row[critic_index]: output_row[films_index]}
        output_rows.append(fav_films)
#print(output_rows)

csv_file = "2021.csv"
csv_columns = ["Critic/Publisher", "Films"]

try:
    with open(csv_file, 'w') as csvfile:
        write = csv.DictWriter(csvfile, fieldnames = csv_columns)
        for row in output_rows:
            for key, value in row.items():
                write.writerow({"Critic/Publisher": key, 'Films': value})
            #need to figure out how to take 'Films' out of list form. Do I want to fieldname 1-10?
        
except IOError:
    print('IOerror')

#TO DO: export output_rows to a csv and make program work over all review years!