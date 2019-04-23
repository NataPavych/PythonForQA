# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:23:54 2019

@author: Nataliya_Pavych
"""

import sqlite3
import requests

current_rates = requests.get('https://api.exchangeratesapi.io/latest').json()['rates']

with sqlite3.connect('forex.sqlite3') as conn:
    print('OLD')
    cursor = conn.cursor()
    cursor.execute('SELECT currency_code, rate FROM rates')
    column_names = [element[0] for element in cursor.description]
    for row in cursor.fetchall():
        print(dict(zip(column_names, row)))
    
    print('UPDATE')
    query_when = ''
    query_in = ''
    for code in current_rates:
        query_when += f"WHEN currency_code = '{code}' THEN {current_rates[code]} "
        query_in += f"'{code}',"
    query = f"UPDATE rates SET rate=  CASE  {query_when} END WHERE currency_code IN ({query_in[:-1]})"
    cursor.execute(query)
    
    print('NEW')
    cursor.execute('SELECT currency_code, rate FROM rates')
    column_names = [element[0] for element in cursor.description]
    for row in cursor.fetchall():
        print(dict(zip(column_names, row)))
    

        