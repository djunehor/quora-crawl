"""Browser Module"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time
import dateparser
import datetime

# Crome driver options
OPTION = Options()

OPTION.add_argument("--disable-infobars")
OPTION.add_argument("start-maximized")
OPTION.add_argument("--disable-extensions")
OPTION.add_argument("--headless")
# disable notifications popup alert
OPTION.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

# specifies the path to the chromedriver
GOOGLE_CHROME_PATH = '/app/.chromedriver/bin/chromedriver'
CHROMEDRIVER_PATH = 'chromedriver.exe'

# initialise
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--disable-gpu')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--ignore-certificate-errors')
# options.binary_location = GOOGLE_CHROME_PATH


class Browser:
    """Browser class"""

    def __init__(self, linux):
        if linux == True:
            self.driver = webdriver.Chrome(executable_path=GOOGLE_CHROME_PATH, options=options,
                                  service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
        else:
            self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=OPTION)

    def get_home(self):
        """Navigates to Quora mainpage"""
        url = "https://www.quora.com"
        self.driver.get(url)
        print("[Browser] Visiting Quora Homepage")

    def get_url(self, url):
        """Navigates to URL"""
        self.driver.get(url)
        print("[Browser] Visited ", url)

    def login(self, username, user_pass):
        form = self.driver.find_element_by_class_name('regular_login')
        email = form.find_element_by_name("email")
        email.send_keys(username)
        password = form.find_element_by_name("password")
        password.send_keys(user_pass)
        password.send_keys(Keys.RETURN)
        time.sleep(3)
        if 'Add Question' in self.driver.page_source:
            print('Quora Login successful')
        else:
            print('Quora Login failed: ', self.driver.title)
            exit()

    def search_by(self, search_keyword):
        """Initiate the search with keyword"""
        self.driver.get("https://www.quora.com/search?q="+search_keyword+"&type=question")
        if 'Search' in self.driver.title:
            print("Search succeeded")
        else:
            print('Something bad has happened: ', self.driver.title)
            exit()

    def infinite_scroll(self):
        for i in range(1, 100):
            try:
                current = self.driver.page_source
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new = self.driver.page_source
                if current == new:
                    return
            except:
                pass

    def get_source(self):
        """Returns current page source html"""
        return self.driver.page_source.encode('utf-8')

    def get_urls(self):
        urls = []
        elems = self.driver.find_elements_by_class_name("question_link")
        for elem in elems:
            urls.append(elem.get_attribute("href"))

        return urls

    def get_comments(self):
        all_comm = []

        comments = self.driver.find_elements_by_class_name('pagedlist_item')

        for comment in comments:
            if 'Sponsored' in comment.text:
                continue
            data = {}
            data['user'] = {}
            try:
                div = comment.find_element_by_class_name('u-serif-font-main--large')
                div.find_element_by_class_name('ui_qtext_more_link').click()
            except:
                pass

            try:
                div = comment.find_element_by_class_name('u-serif-font-main--large')
                data['text'] = div.text
            except:
                continue

            try:
                user = comment.find_element_by_css_selector('a')

                if user:
                    data['user']['url'] = user.get_attribute('href')
                    data['user']['name'] = user.text
            except:
                pass

            try:
                text = comment.find('a', class_="_1sA-1jNHouHDpgCp1fCQ_F").get_text()
                data['user']['datetime'] = str(dateparser.parse(text))
            except:
                data['user']['datetime'] = str(datetime.datetime.now())
            all_comm.append(data)

        return all_comm

