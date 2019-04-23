<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:54:45 2019

@author: Nataliya_Pavych
"""

import argparse
import csv
import collections
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_file', help='name of input file')
parser.add_argument('-c', '--pattern_file', help='name of file with providers')
#parser.add_argument('-p', '--providers', type=str, nargs='+', help='name of providers you need')
parser.add_argument('-o', '--output_file', help='name of output file ')
args = parser.parse_args()
#provider = [args.providers]

# Input providers
n = int(input('How many providers do you need ? \n'))
provider = []
i = 0
while i < n:
    pr = input(f'provider {i+1}: ')
    provider.append(pr)
    i += 1
print(provider)

# get phones from input file
phone_regex = re.compile(r'[+(\d{1,}]?[0-9 .\-()]{7,}[0-9]')
parsed_phone = []
with open(args.input_file, encoding='utf-8') as text_file:
    for line in text_file:
        phone = phone_regex.search(line)
        if phone is not None:
            parsed_phone.append(phone.group())

# create pattern dictionary
pattern_dict = collections.defaultdict(collections.Counter)
with open(args.pattern_file, newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        pattern_dict[row['number_pattern'].replace(' ', '').replace('x', '')] = row['provider']

# match phones with patterns
phones = {}
for raw_phone in parsed_phone:
    phone = raw_phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "").replace("+3", "").lstrip('8').lstrip('0')
    phones[raw_phone] = pattern_dict.get(phone[:3]) or pattern_dict.get(phone[:2])

# write phones in a file
with open(args.output_file, 'w', newline='') as csv_file:
    field_names = ['phone', 'provider']
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    for key, value in phones.items():
        if value in provider:
            writer.writerow({'phone': key, 'provider': value})
=======
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:54:45 2019

@author: Nataliya_Pavych
"""

import argparse
import csv
import collections
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_file', help='name of input file')
parser.add_argument('-c', '--pattern_file', help='name of file with providers')
#parser.add_argument('-p', '--providers', type=str, nargs='+', help='name of providers you need')
parser.add_argument('-o', '--output_file', help='name of output file ')
args = parser.parse_args()
#provider = [args.providers]

# Input providers
n = int(input('How many providers do you need ? \n'))
provider = []
i = 0
while i < n:
    pr = input(f'provider {i+1}: ')
    provider.append(pr)
    i += 1
print(provider)

# get phones from input file
phone_regex = re.compile(r'[+(\d{1,}]?[0-9 .\-()]{7,}[0-9]')
parsed_phone = []
with open(args.input_file, encoding='utf-8') as text_file:
    for line in text_file:
        phone = phone_regex.search(line)
        if phone is not None:
            parsed_phone.append(phone.group())

# create pattern dictionary
pattern_dict = collections.defaultdict(collections.Counter)
with open(args.pattern_file, newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        pattern_dict[row['number_pattern'].replace(' ', '').replace('x', '')] = row['provider']

# match phones with patterns
phones = {}
for raw_phone in parsed_phone:
    phone = raw_phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "").replace("+3", "").lstrip('8').lstrip('0')
    phones[raw_phone] = pattern_dict.get(phone[:3]) or pattern_dict.get(phone[:2])

# write phones in a file
with open(args.output_file, 'w', newline='') as csv_file:
    field_names = ['phone', 'provider']
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    for key, value in phones.items():
        if value in provider:
            writer.writerow({'phone': key, 'provider': value})
>>>>>>> Task1-LogProcessing
