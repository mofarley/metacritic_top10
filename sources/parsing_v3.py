import os
from bs4 import BeautifulSoup
import csv
with open("/home/moses/Desktop/metacritic_top10/metacritic_films/sources/Film Critic Top 10 Lists - Best Movies of 2017 - Metacritic.html", "r") as f:
    #TO DO: os path for htmls
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
    #critics_and_films_total = # of <tr>'s in a given table or tablebody tag
    publisher_name = table.find('caption').text
    while count < critics_and_films_total:
        temp_row = []
        #use count as an index value for critics and films that fall under <tr>'s
        for i in range(2):
            flag = False
            if count % 2 != 0: #if count is odd or represents the film list rather than critic name.
                film_list = critics_and_films[count].find_all('li')
                tie_critic = False
                for flic in film_list:
                    try:
                        x = int(flic['value'])
                        if x in range(11):                            
                            if '(tie)' in flic.text:
                                tie_critic = True
                                no_tie = flic.text
                                no_tie = no_tie.replace('(tie)','').strip()
                                tie_split = no_tie.split(' AND ')
                                for tied_movie in tie_split:
                                    tied_movie.strip()
                                    temp_row.append(tied_movie.strip())
                            else:
                                temp_row.append(flic.text)
                        else:
                            flag = True
                            continue
                    except (KeyError, ValueError) as e:
                        #exception looking for film list not existing or no 'value' attribute
                        flag = True
                        continue
            else:
                critic_name = critics_and_films[count].text
            # print('{}  {}'.format(count, critics_and_films[count]))
            # add unformated critic and their films to temp row (output_row)
            if i == 1 and flag == False:
                temp_row.insert(0, critic_name)
            count += 1
        if len(temp_row) > 9:
            critic = temp_row[0].replace("View full list", "").strip('\n').strip()
            if critic == 'Staff consensus':
                temp_row[0] = publisher_name.strip()
            elif critic == 'Staff':
                temp_row[0] = publisher_name.strip()
            else:
                temp_row[0] = critic
            output_rows.append(temp_row)


csv_file = "2017.csv"
csv_columns = ["Critic/Publisher", "First", 'Second', 'Third', 'Fourth', 'Fifth',
'Sixth', 'Seventh', 'Eigth', 'Ninth', 'Tenth']

try:
    with open(csv_file, 'w') as csvfile:
        csvwrite = csv.writer(csvfile)
        csvwrite.writerow(csv_columns)
        csvwrite.writerows(output_rows)
except IOError:
    print('IOerror')
