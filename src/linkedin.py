import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Function to create and connect to the webdriver (used for getting linkedin data)
def connect_to_webdriver():
   # sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome(r'C:\Users\marin\Desktop\chromedriver.exe',chrome_options=chrome_options)
    return wd

# Function to sign into linkedin account
def sing_into_linkedin(email, password, web_driver):
    web_driver.get("https://www.linkedin.com/login")
    login_element = web_driver.find_element_by_name('session_key')
    login_element.send_keys(email)
    time.sleep(0.5)
    login_element = web_driver.find_element_by_name('session_password')
    login_element.send_keys(password)
    time.sleep(0.5)
    login_element.submit()

# Function to check if sign in was successful
def check_sign_in(web_driver):
    if not web_driver.current_url.__contains__('feed'):
        print("Enter PIN: ")
        pin = input()
        element = web_driver.find_element_by_name('pin')
        element.send_keys(pin)
        time.sleep(1)
        element.submit()

# Function to scrap the data from linkedin profile
def get_linkedin_data(url, web_driver): 
    page_url = url
    data = []
    if page_url.endswith('/'):
        about_page = page_url + 'about'
    else:
        about_page = page_url + '/about'
    web_driver.get(about_page)
    html_text = web_driver.page_source
    parser = BeautifulSoup(html_text, 'html5lib')
    about_data_loc = parser.find_all('dd', {'class': 'org-page-details__definition-text t-14 t-black--light t-normal'})
    overview = parser.find('p')
    if overview is not None:
        data.append(overview.get_text().strip('\n '))
    if about_data_loc is None:
        return data
    for loc in about_data_loc:
        if loc.find('a') is not None:
            a = loc.find('a')
            data.append(a.get('href'))
        else:
            data.append(loc.get_text().strip('\n '))
    return data

# Helper function to check if link is valid
def check_linkedin_url(url):
    page_url = url
    if(str(page_url).__contains__('company/')):
        return True
    return False

