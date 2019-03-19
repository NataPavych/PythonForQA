# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 17:07:04 2019

@author: Nataliya_Pavych
"""


def load_file_into_list_by_line(file_name: str) -> object:
    with open(file_name) as text_file:
        return [line for line in text_file]


def clean_data_into_d2_list(list_name):
    return list(map(lambda string: (lambda x, y, z: [f'{x} {y[1:12]}', int(z)])(*string.split(' ')), list_name))


def get_hours_from(list_name):
    return list(map(lambda string: string.split(':')[1], list_name))


def sum_values_by_key_into_dictionary(list_name):
    dictionary = {}
    for element in list_name:
        if element[0] in dictionary:
            dictionary.update({element[0]: dictionary[element[0]]+element[1]})
        else:
            dictionary.update({element[0]: element[1]})
    return dictionary


def max_value_by_partial_key(income_dictionary):
    outcome_dictionary = {}
    for key, value in income_dictionary.items():
        [key1, key2, value] = *key.split(' '), value
        if key2 in outcome_dictionary:
            if outcome_dictionary[key2][1] < value:
                outcome_dictionary.update({key2: (key1, value)})
            else:
                outcome_dictionary.update({key2: outcome_dictionary[key2]})
        else:
            outcome_dictionary.update({key2: (key1, value)})
    return outcome_dictionary


def count_duplicates_into_dictionary(list_name):
    dictionary = {}
    for element in list_name:
        if element in dictionary:
            dictionary.update({element: dictionary[element]+1})
        else:
            dictionary.update({element: 1})
    return dictionary
               

def print_dictionary(dictionary_name):
    for key, value in dictionary_name.items():
        print(f'{key}   -    {value}')


def print_dictionary_partial_value(dictionary_name, n):
    for key, value in dictionary_name.items():
        print(f'{key}   -    {value[n]}')


# Load and clean data
raw_data = load_file_into_list_by_line("log_data/log_data.txt")
cleaned_data = clean_data_into_d2_list(raw_data)

# Find the top downloader for each date
sum_by_ip_date = sum_values_by_key_into_dictionary(cleaned_data)
max_by_date = max_value_by_partial_key(sum_by_ip_date)
print_dictionary_partial_value(max_by_date, 0)
print()

# Find the least busy hour – the hour that has the least number of requests 
hours_list = get_hours_from(raw_data)
hours_count = count_duplicates_into_dictionary(hours_list)
min_hour = min(hours_count, key=hours_count.get)
print(f'The least busy hour is {min_hour}')
