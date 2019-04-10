# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 18:09:49 2019

@author: Nataliya_Pavych
"""

import argparse
import requests
import os
import bs4


def download_avatar(directory, request_response):
    with open(os.path.join(f'{directory}', os.path.basename(url)), 'wb') as image_file:
        for chunk in request_response.iter_content(chunk_size=1024):
            image_file.write(chunk)
    
            
def extract_download_avatar(full_url, directory):
    response = requests.get(full_url)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        web_object = soup.select('img')
        for image_number in range(len(web_object)):
            image_url = web_object[image_number].get('src')
            if ['.jpg', '.png'] not in str(image_url):
                continue
            if not str(image_url).startswith('https://'):
                image_url = 'https://' + str(image_url)
            avatar_response = requests.get(image_url, stream=True)
            if avatar_response.status_code == 200:
                download_avatar(directory, avatar_response)


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username in GitHub')
parser.add_argument('-p', '--project', help='username_project you need')
args = parser.parse_args()

folder = str(f'D:/{args.username}/{args.project}')
os.makedirs(folder, exist_ok=True)

url_string = str(f'https://github.com/{args.username}/{args.project}')
response = requests.get(url_string, stream=True)
response.status_code
if response.status_code == 200:
    extract_download_avatar(url_string, folder)
