from bs4 import BeautifulSoup
import csv
with open("metacritic_films/sources/Film Critic Top 10 Lists - Best Movies of 2015 - Metacritic.html", "r") as f:
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
            if count % 2 != 0:
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
            else:
                temp_row[0] = critic
            output_rows.append(temp_row)

csv_file = "2015.csv"
csv_columns = ["Critic/Publisher", "First", 'Second', 'Third', 'Fourth', 'Fifth',
'Sixth', 'Seventh', 'Eigth', 'Ninth', 'Tenth']

try:
    with open(csv_file, 'w') as csvfile:
        csvwrite = csv.writer(csvfile)
        csvwrite.writerow(csv_columns)
        csvwrite.writerows(output_rows)
except IOError:
    print('IOerror')
#TO DO: ...
