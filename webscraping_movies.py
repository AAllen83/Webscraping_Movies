import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_25'
csv_path = '/home/project/top_25_films.csv'
df = pd.DataFrame(columns=["Film","Year","Rotten Tomatoes' Top 100"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

tables = data.find_all('tbody')                              #gets the body of all the tables in the web page
rows = tables[0].find_all('tr')                              #gets all the rows of the first table

for row in rows:                                             #Iterate over the contents of the variable rows.'''
    if count<25:                                             #Check for the loop counter to restrict to 50 entries.'''
        col = row.find_all('td')                             #Extract all the td data objects in the row and save them to col.'''
        if len(col)!=0:                                      #Check if the length of col is 0, that is, if there is no data in a current row. This is important since, many timesm there are merged rows that are not apparent in the web page appearance.'''
            data_dict = {"Film": col[1].contents[0],         #Create a dictionary data_dict with the keys same as the columns of the dataframe created for recording the output earlier and corresponding values from the first three headers of data.'''
                         "Year": col[2].contents[0],
                         "Rotten Tomatoes' Top 100": col[3].contents[0]}
            df1 = pd.DataFrame(data_dict, index=[0])         #Convert the dictionary to a dataframe'''
            #df2 = df1[df1['Year'] > '1999']		         #PYTHON NOT ACCEPTING THIS LINE OF CODE
            df = pd.concat([df,df2], ignore_index=True)      #concatenate it with the existing one'''
            count+=1                                         #Increment the loop counter.'''
    else:                                                    #Once the counter hits 25, stop iterating over rows and break the loop.'''
        break

print(df)

df.to_csv(csv_path)                                          #save it to a CSV'''

conn = sqlite3.connect(db_name)                              #initialize a connection to the database'''
df.to_sql(table_name, conn, if_exists='replace', index=False)#save the dataframe as a table'''
conn.close()                                                 #close the connection'''