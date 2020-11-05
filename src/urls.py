import os
import re
import time
import requests

# Helper function to filter urls
def filter_urls(urls):
    filtered_urls = [re.sub(".\n", "", url) for url in urls]
    return filtered_urls

# Helper function to get urls from a csv file
def get_urls(directory, file_name):
    urls = []
    with open(os.path.join(directory, file_name), 'r') as file:
        for line in file.readlines():
            urls.append(line)
    urls = filter_urls(urls)
    return urls

# Function to get the plain text of a url
def get_plain_text(url):
    time.sleep(0.01)
    headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
                }
    code = requests.get(url, headers = headers, verify = False, timeout = 10)
    text = code.text
    return text
    