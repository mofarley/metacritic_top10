from bs4 import BeautifulSoup
import csv
from critic_list import list_critics
with open("/Users/mosesfarley/metacritic_top10/metacritic_films/sources/Film Critic Top 10 Lists - Best of 2012 - Metacritic.html", "r") as f:
    topten = BeautifulSoup(f, "html.parser")

tables = topten.find_all("table")
#eventually change tables to find_all. Also remember find_all returns a set.
output_rows = []
#output_rows = final list that's converted to csv
for table in tables:
    critics_and_films = table.find_all("tr") 
    #critics_and_films --> see line 14 on parsing_notes.txt
    num_rows = len(critics_and_films)
    critics_and_films_total = int(num_rows / 2) 
    #critics_and_films_total = # of <tr>'s in a given table or tablebody tag
    #publisher_name = table.find('caption').text
    temp_row = []
    count = 0
    #use count as an index value for critic_index and films that fall under <tr>'s
    while count < num_rows:
        for i in range(2):
            flag = False
            if i == 1:
                film_list = critics_and_films[count].find_all('li')
                for flic in film_list:
                    try:
                        x = int(flic['value'])
                        if x in range(11):
                            temp_row.append(flic.text)
                        else:
                            flag = True
                            continue
                    except (KeyError, ValueError) as e:
                        #exception looking for film list not existing or no 'value' attribute
                        flag = True
                        continue
                count += 1
            else:
                critic_name = critics_and_films[count].text
                count += 1
            # print('{}  {}'.format(count, critics_and_films[count]))
            # add unformated critic and their films to temp row (output_row)
            if i == 1 and flag == False:
                temp_row.insert(0, critic_name)
        if len(temp_row) > 9:
            critic = temp_row[0].replace("View full list", "").strip('\n').strip()
            critic = critic.replace("View article", "").strip()
            #critic_list = list_critics()
            #for critic_name in critic_list:
                #if critic_name in critic:
                    #critic = critic_name
            if critic == 'Staff consensus':
                temp_row[0] = 'fix later'
            else:
                temp_row[0] = critic
            output_rows.append(temp_row)
            temp_row = []

critic_list = list_critics()

for x in output_rows:
    for critic_name in critic_list:
        if critic_name in x[0]:
            x[0] = critic_name
        elif 'Staff consensus' in x[0]:
            x[0] = x[0].replace('Staff consensus', '').strip()
    



csv_file = "2013_test.csv"
csv_columns = ["Critic/Publisher", "First", 'Second', 'Third', 'Fourth', 'Fifth',
'Sixth', 'Seventh', 'Eigth', 'Ninth', 'Tenth']

try:
    with open(csv_file, 'w') as csvfile:
        csvwrite = csv.writer(csvfile)
        csvwrite.writerow(csv_columns)
        csvwrite.writerows(output_rows)
except IOError:
    print('IOerror')