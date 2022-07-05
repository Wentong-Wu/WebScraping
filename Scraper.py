from lib2to3.pgen2 import driver
from turtle import delay
import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class Scraper:

    def __init__(self) -> webdriver.Edge:
        self.driver = webdriver.Edge() 
        self.URL = "https://store.eu.square-enix-games.com/en_GB/"
        self.driver.get(self.URL)
        self.delay = 10
        pass 

    def load_and_accept_cookies(self):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-banner-sdk"]')))
            print("Frame Ready!")
            #driver.switch_to.frame('onetrust-banner-sdk')
            accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            print("Accept Cookies Button Ready!")
            time.sleep(3)
            accept_cookies_button.click()
        except TimeoutException:
            print("Loading took too much time!")
        return self.driver
    
    def scraping_one_data(self):
        self.load_and_accept_cookies()
        list_of_links = []
        time.sleep(2)
        #elements = self.driver.find_elements(By.XPATH,'//a[@class="product-link-box"]')
        elements = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="product-link-box"]')))
        for elem in elements:
            list_of_links.append(elem)
        print(list_of_links)
        time.sleep(3)
        list_of_links[4].click()
        # suselements = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@aria-hidden="false"]')))
        # print(suselements)
        pass

    def get_sale():
        driver = webdriver.Edge()
        URL = "https://store.eu.square-enix-games.com/en_GB/digital-sale"
        driver.get(URL)
        time.sleep(5)
        length_of_page = driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
        page_end = False
        while(page_end==False):
            last_length_page = length_of_page
            time.sleep(3)
            length_of_page = driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
            if last_length_page==length_of_page:
                page_end=True
    
    def get_all_games():
        driver = webdriver.Edge()
        URL = "https://store.eu.square-enix-games.com/en_GB/games/all-games"
        driver.get(URL)
        time.sleep(5)
        length_of_page = driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
        page_end = False
        while(page_end==False):
            last_length_page = length_of_page
            time.sleep(3)
            length_of_page = driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
            if last_length_page==length_of_page:
                page_end=True

web = Scraper()
web.scraping_one_data()