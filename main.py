from src.query import *
from src.data import *
from src.urls import *
from src.linkedin import *
import pandas as pd
import os
import csv
from googlesearch import search
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys
from selenium import  webdriver
import requests

def main():
    query = 'חברת שליחויות'
    query_results = search_query(query, 100, 100)
    current_dir = os.getcwd()
    file_name = 'Query Results.csv'
    output_csv(current_dir, file_name, query_results)
    urls = get_urls(current_dir, file_name)
    # web_driver = connect_to_webdriver()
    # connect_to_linkedin('', '')
    data = []
    for url in urls:
        single_data_point = []
        print(url)
        try:
            html_text = get_plain_text(url)
            single_data_point = []
            single_data_point.append(get_company_names(url))
            single_data_point.append(url)
            single_data_point.append(get_social_media(html_text))
            single_data_point.append(search_email(html_text))
            single_data_point.append(get_number(html_text))
            linkedin_url = get_linkedin(html_text)
            single_data_point.append(linkedin_url)
            #for link in linkedin_url:
            #    if check_linkedin_url(link):
            #        single_data_point.append(get_linkedin_data(link))
            data.append(single_data_point)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
    
    fields = ['Company name', 'URL', 'Social Media', 'Email', 'Telephone', 'Linkedin', 'Linkedin data']
    output_csv(current_dir, 'data.csv', fields=fields, data=data)

if __name__ == '__main__':
    main()