import os
import csv
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime

EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
PHONE_REGEX = r"""^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"""

def output_query(directory, file_name, query_results):
    if not os.path.exists(directory):
        os.mkdir(directory)
    with open(os.path.join(directory, file_name), 'w') as file:
        file.writelines(query_results)

def save_results(directory, file_name, results):
    if not os.path.exists(directory):
        os.mkdir(directory)
    with open(os.path.join(directory, file_name), 'w') as file:
        for site in results:
            for data in site:
                file.writelines(data + '\n')

def output_csv(fields, data):
    name = "data"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([name, suffix])
    filename += ".csv"
    data_frame = pd.DataFrame(data, columns=fields)
    data_frame.to_csv(filename)


def search_email(url):
    html_text = url
    found_emails = [match.group(0) for match in re.finditer(EMAIL_REGEX, html_text)] 
    found_emails = remove_duplicates(found_emails)
    return found_emails

def filter_data2(lst):
    lst = [item for item in lst if item != []]
    return lst

def search_number(text):
    html_text = text
    found_numbers = [match.group(0) for match in re.finditer(PHONE_REGEX, html_text)]
    found_numbers = remove_duplicates(found_numbers)
    return found_numbers

def get_social_media(text):
    html_text = text
    html_parser = BeautifulSoup(html_text, "html.parser")
    subtree = html_parser.findAll('a')
    hrefs = [item.get('href') for item in subtree]
    hrefs = [link for link in hrefs if link != None]
    social_media = [link for link in hrefs 
                    if str(link).__contains__('facebook') or
                    str(link).__contains__('instagram') or 
                    str(link).__contains__('whatsapp') or
                    str(link).__contains__('twitter')
                    ]
    social_media = remove_duplicates(social_media)
    return social_media

def get_linkedin(text):
    html_text = text
    html_parser = BeautifulSoup(html_text, "html.parser")
    subtree = html_parser.findAll('a')
    hrefs = [item.get('href') for item in subtree]
    hrefs = [link for link in hrefs if link != None]
    linkedin = [link for link in hrefs if str(link).__contains__('linkedin')]
    linkedin = remove_duplicates(linkedin)
    return linkedin

def get_number(text):
    html_text = text
    html_parser = BeautifulSoup(html_text, "html.parser")
    subtree = html_parser.findAll('a')
    hrefs = [item.get('href') for item in subtree]
    hrefs = [link for link in hrefs if link != None]
    numbers = [number for number in hrefs if str(number).__contains__('tel') or
                str(number).__contains__('number')]
    numbers = remove_duplicates(numbers)
    return numbers

def remove_duplicates(list):
    no_duplicates = []
    for i in list:
        if i not in no_duplicates:
            no_duplicates.append(i)
    return no_duplicates