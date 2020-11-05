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

# Main function that runs the entire script
def main():
    print("Enter your query: ")
    query = input() # חברת שליחויות
    query_results = search_query(query, 100, 100)
    current_dir = os.getcwd()
    file_name = 'Query Results.csv'
    save_output(current_dir, file_name, query_results)
    urls = get_urls(current_dir, file_name)
    print("Do you also want to search linkedin data? [yes/no]")
    response = input()
    flag = False
    if response.lower() == 'yes' or response.lower() == 'y':
        flag = True
        print("Enter linkedin email: ")
        email = input()
        print("Enter linkedin password: ")
        password = input()
        web_driver = connect_to_webdriver()
        sing_into_linkedin(email, password, web_driver)
        check_sign_in(web_driver)
    else:
        pass
    
    data = []
    for url in urls:
        single_data_point = []
        print(url)
        try:
            html_text = get_plain_text(url)
            single_data_point = []
            single_data_point.append(get_company_names(url))
            single_data_point.append(url)
            single_data_point.append(search_social_media(html_text))
            single_data_point.append(search_email(html_text))
            single_data_point.append(get_number(html_text))
            linkedin_url = get_linkedin(html_text)
            single_data_point.append(linkedin_url)
            if flag:
                for link in linkedin_url:
                    if check_linkedin_url(link):
                        single_data_point.append(get_linkedin_data(link, web_driver))
            data.append(single_data_point)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
    if flag:
        web_driver.close()
        fields = ['Company name', 'URL', 'Social Media', 'Email', 'Telephone', 'Linkedin', 'Linkedin data']
        output_csv(fields, data)
    else:
        fields = ['Company name', 'URL', 'Social Media', 'Email', 'Telephone', 'Linkedin']
        output_csv(fields, data)

if __name__ == '__main__':
    main()
