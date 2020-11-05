import os
import re
import time
import requests
from urllib.parse import urlparse

def filter_urls(urls):
    filtered_urls = [re.sub(".\n", "", url) for url in urls]
    return filtered_urls

def get_urls(directory, file_name):
    urls = []
    with open(os.path.join(directory, file_name), 'r') as file:
        for line in file.readlines():
            urls.append(line)
    urls = filter_urls(urls)
    return urls

def get_plain_text(url):
    time.sleep(0.01)
    headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
                }
    code = requests.get(url, headers = headers, verify = False, timeout = 10)
    text = code.text
    return text

def get_company_names(url):
    parsed = urlparse(url)
    intermediary_name = parsed.netloc
    if url.__contains__('www'):
        return intermediary_name.split('.')[1]
    else:
        return intermediary_name.split('.')[0]

