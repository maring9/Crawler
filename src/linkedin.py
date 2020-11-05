def connect_to_webdriver():
    sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    return wd

def connect_to_linkedin(email, password):
    wd.get("https://www.linkedin.com/login")
    login_element = wd.find_element_by_name('session_key')
    login_element.send_keys(email)
    time.sleep(0.5)
    login_element = wd.find_element_by_name('session_password')
    login_element.send_keys(password)
    time.sleep(0.5)
    login_element.submit()

def get_linkedin_data(url): 
    page_url = url
    data = []
    if page_url.endswith('/'):
        about_page = page_url + 'about'
    else:
        about_page = page_url + '/about'
    wd.get(about_page)
    html_text = wd.page_source
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

def check_linkedin_url(url):
    page_url = url
    if(str(page_url).__contains__('company/')):
        return True
    return False

