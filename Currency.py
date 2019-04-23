# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:11:01 2019

@author: Nataliya_Pavych
"""

import sqlite3
import requests
import csv


def get_json_from(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()


def get_currency(db_file):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT currency_code, rate FROM rates')
        currency = {}
        for row in cursor.fetchall():
            currency[row[0]] = row[1]
        conn.commit()    
        return currency


def minus(dict1, dict2):
    res = dict1.keys() - dict2.keys()
    return {key: dict1[key] for key in res}

def compare_same(dict1, dict2):  # get the same key:value
    return dict(set(dict1.items()) & set(dict2.items()))


def write_row(line, file):
    file.write(line)


def in_condition(list_name):
    query_in = ''
    for elenemt in list_name:
       query_in += f"'{elenemt}',"
    return f'IN ({query_in[:-1]})'   
codes = ('BGN','NZD','ILS','RUB','PLN')
print(in_condition(codes))


def select_query(table_name, column_list):
    columns = ''
    for elenemt in column_list:
        columns += f'{elenemt},'
    return f'SELECT {columns[:-1]} FROM {table_name}'
table_name = 'rates'
column_list = ('currency_code', 'rate')
select_query(table_name, column_list)


def delete_in_query(table_name, column_name, in_list):
    return f'DELETE FROM {table_name}  WHERE {column_name} {in_condition(in_list)}'
table_name = 'rates'
column_name = 'code'
codes = ['BGN','NZD','ILS','RUB','PLN']
delete_in_query(table_name, column_name, codes)


def update_query(table_name, set_col, where_col, key_value_pair):
    query = f'UPDATE {table_name} SET {set_col} = '
    for key, value in key_value_pair.items():
         query += f"{value} WHERE {where_col} = '{key}'"
    return f'{query}'
key_value_pair = {'BGN': 1.9558}
table_name = 'rates'
set_column = 'rate'
where_col = 'currency_code'
update_query(table_name, set_column, where_col,  key_value_pair)


def insert_query(table_name, column_list, values):
    val = '?,'*len(values)
    columns = ''
    for elenemt in column_list:
        columns += f'{elenemt},'
    return f'INSERT INTO {table_name}({columns[:-1]}) VALUES ({val[:-1]})'
table_name = 'rates'
column_list = ['currency_code','rate']
values = ('BGN', 1.9558)
insert_query(table_name, column_list, values)


def percent_change(old,new):
    return round((new/old)*100-100,2)
percent_change(1.1321,1.15)
    

exchangerate = get_json_from('https://api.exchangeratesapi.io/latest')
currency_new = exchangerate['rates']
db_name = 'forex.db'
currency_old = get_currency(db_name)

table_name = 'rates'
column_name = 'currency_code'
set_column = 'rate'
work_columns = ['currency_code','rate']

stable_data = compare_same(currency_old, currency_new)

insert_data = minus(currency_new, currency_old)
insert_values = [(code, value) for code, value in insert_data.items()]

delete_data = minus(currency_old, currency_new)

update_data = minus(minus(minus(currency_new, insert_data),delete_data),stable_data)

with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    table_name = 'rates'
    work_columns = ['currency_code','rate']
    set_column = 'rate'
    where_colunm = 'currency_code'
    cursor.execute(select_query(table_name, work_columns))
    with open('rates_report.csv', 'a') as report_file:
        writer = csv.writer(report_file)
        headers = ['currency_code', 'old_rate', 'new_rate', 'percent_change']
        writer.writerow(headers)
        #write_row(headers, report_file)
        for row in cursor.fetchall():
            #print(row)
            for code in update_data:
                if code == row[0]:
                    new_value = update_data[code]
                    #print(code, row[1], new_value, percent_change(row[1],new_value))
                    writer.writerow([code, row[1], new_value, percent_change(row[1],new_value)])
                    key_value_pair = {code: update_data[code]}
                    #print(update_query(table_name, set_column, where_colunm, key_value_pair)) 
                    cursor.execute(update_query(table_name, set_column, where_colunm, key_value_pair))
    for values in insert_values:
        #print(insert_query(table_name, work_columns, insert_values))
        cursor.execute(insert_query(table_name, work_columns, values), values)
    #delete_in_query(table_name, where_colunm, [code for code in delete_data])
    cursor.execute(delete_in_query(table_name, where_colunm, [code for code in delete_data]))
    conn.commit()
    cursor.execute('SELECT * FROM rates')
    column_names = [element[0] for element in cursor.description]
    print(column_names)
    for row in cursor.fetchall():
        print(row)
    conn.commit()
