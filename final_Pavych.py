# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:02:05 2019

@author: Nataliya_Pavych
"""

import datetime
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import pyodbc 
import numpy
import matplotlib.pyplot as plt
import matplotlib as mpl

# get data from request into dataframe
start_date = datetime.date(2017,1,1)
end_date = datetime.date(2017,12,31)
date_range = end_date - start_date
data = pd.DataFrame()
for i in range(date_range.days + 1):
    post_day = start_date + datetime.timedelta(i)
    print(f'https://35.204.204.210/{post_day}/')
    response = requests.get(f'https://35.204.204.210/{post_day}/', verify=False)
    json_data = json.loads(response.text)
    for record in json_data.values():
        temp_data = json_normalize(record)
    data = data.append(temp_data, ignore_index = True)   
 
# convert datatypes
data['total_area'] = data['total_area'].fillna(0).astype(numpy.int64)
data['kitchen_area'] = data['kitchen_area'].fillna(0).astype(numpy.int64)
data['living_area'] = data['living_area'].fillna(0).astype(numpy.int64)
data['number_of_rooms'] = data['number_of_rooms'].fillna(0).astype(numpy.int64)
data['added_on'] =pd.to_datetime(data.added_on)

#insert data into SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=EPUALVIW0303;'
                      'Database=Study;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
for index,row in data.iterrows():
    cursor.execute("INSERT INTO dbo.Posting([PriceUSD],[Title],[Text],[TotalArea],[KitchenArea],[LivingArea], [Location],[NumberRooms],[AddedOn]) values (?,?,?,?,?,?,?,?,?)", 
                 row['price_usd'], row['title'], row['text'],
                 row['total_area'], row['kitchen_area'], row['living_area'],
                 row['location'], row['number_of_rooms'], row['added_on']
                 ) 
    conn.commit()
cursor.close()

# get dataset for report
query_data = pd.read_sql_query(
'''SELECT COUNT(*) AS PostCount
     , Month(AddedOn) AS Month
	 , NumberRooms AS NumberOfRooms
   FROM Posting
   GROUP BY Month(AddedOn)
	   , NumberRooms
   HAVING NumberRooms BETWEEN 1 AND 5
   ORDER BY Month
        ,NumberOfRooms''', conn)

#pivot dataset
report_data = pd.pivot_table(query_data, values='PostCount', 
                                         index='Month', 
                                         columns='NumberOfRooms')
# plot 
report_data.plot()
plt.ylabel('Number of OLX posts by number of rooms')
plt.savefig('Number_of_Rooms-2017.png')

