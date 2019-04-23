# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:11:01 2019

@author: Nataliya_Pavych
"""

import sqlite3
import requests


response = requests.get('https://api.exchangeratesapi.io/latest')
response.status_code
response.raise_for_status()
exchangerate = response.json()
print(exchangerate)
current_rates = exchangerate['rates']

with sqlite3.connect('forex.sqlite3') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rates')
    column_names = [element[0] for element in cursor.description]
    with open('rates_report.csv', 'w', newline='') as csv_file:
        field_names = ['currency_code', 'old_rate', 'new_rate', 'percent_change']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for row in cursor.fetchall():
             for key, value in current_rates.items():
                if row[1] == key and row[3] != value:
                    row[3] = value
                    cursor.execute('UPDATE rates SET rate = value')
                writer.writerow({'currency_code': key, 
                                     'old_rate': row[3], 
                                     'new_rate': value, 
                                     'percent_change': (row[3])/value)*100-100                   
             print(row) 
    conn.commit()       
                    
                    
