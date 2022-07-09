from argparse import Action
from cgi import print_arguments
from lib2to3.pgen2 import driver
from math import prod
from os import link
from re import M
from turtle import delay
from unicodedata import name
import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

class Scraper:

    def __init__(self) -> webdriver.Edge:
        self.driver = webdriver.Edge() 
        self.URL = "https://store.eu.square-enix-games.com/en_GB/"
        self.driver.get(self.URL)
        self.delay = 10
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
        pass 

    # def load_and_accept_cookies(self):
    #     try:
    #         WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-banner-sdk"]')))
    #         print("Frame Ready!")
    #         #driver.switch_to.frame('onetrust-banner-sdk')
    #         accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
    #         print("Accept Cookies Button Ready!")
    #         time.sleep(3)
    #         accept_cookies_button.click()
    #     except TimeoutException:
    #         print("Loading took too much time!")
    #     return self.driver
    
    def get_merch_product(self, list_of_links):
        #self.load_and_accept_cookies()
        time.sleep(2)
        #elements = self.driver.find_elements(By.XPATH,'//a[@class="product-link-box"]')
        a = ActionChains(self.driver)
        m = self.driver.find_element(By.XPATH,'//li[@id="merchandise"]')
        a.move_to_element(m).perform()
        n = self.driver.find_element(By.XPATH,'//li[@id="all-merchandise"]')
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//li[@id="all-merchandise"]')))
        a.move_to_element(n).click().perform()
        time.sleep(2)

        #Scroll all the way down to get all the products
        length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
        page_end = False
        while(page_end==False):
            last_length_page = length_of_page
            time.sleep(3)
            length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
            if last_length_page==length_of_page:
                page_end=True

        #Gets all the link to the products
        elements = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="product-link-box"]')))
        for elem in elements:
            list_of_links.append(elem.get_attribute('href'))
        time.sleep(3)
        return list_of_links
    
    def get_game_product(self, list_of_links):
        #self.load_and_accept_cookies()
        time.sleep(2)
        #elements = self.driver.find_elements(By.XPATH,'//a[@class="product-link-box"]')
        a = ActionChains(self.driver)
        m = self.driver.find_element(By.XPATH,'//li[@id="games"]')
        a.move_to_element(m).perform()
        n = self.driver.find_element(By.XPATH,'//li[@id="all-games"]')
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//li[@id="all-games"]')))
        time.sleep(1)
        a.move_to_element(n).click().perform()
        time.sleep(2)
        #Scroll all the way down to get all the products
        length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
        page_end = False
        while(page_end==False):
            last_length_page = length_of_page
            time.sleep(3)
            length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
            if last_length_page==length_of_page:
                page_end=True

        #Gets all the link to the products
        elements = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="product-link-box"]')))
        for elem in elements:
            list_of_links.append(elem.get_attribute('href'))
        time.sleep(3)
        return list_of_links
    
    def get_all_product_links(self, list_of_links=[]):
        self.get_game_product(list_of_links)
        self.get_merch_product(list_of_links)
        self.all_links = list_of_links
        return list_of_links

    def get_one_data(self, one_link,product_single_dict):
        #get pass age restriction if there is any
        self.driver.get(one_link)
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="birthday_popup"]')))
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//select[@data-internal-id='birthday-day']/option[text()='1']").click()
            self.driver.find_element(By.XPATH, "//select[@data-internal-id='birthday-month']/option[text()='January']").click()   
            self.driver.find_element(By.XPATH, "//select[@data-internal-id='birthday-year']/option[text()='2004']").click()
            self.driver.find_element(By.XPATH, "//button[@data-internal-id='save-birthday']").click()
        except TimeoutException:
            print("Content Valid")
        #get data from the page
        product_title = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "product-title"))).get_attribute("textContent"))
        try:
            product_price = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@data-internal-id='product-strike-through']"))).get_attribute("textContent"))
        except:
            product_price = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@data-internal-id='product-price']"))).get_attribute("textContent"))
        #product_status
        product_status = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buy_button']"))).get_attribute("textContent"))
        #product_image
        product_image = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='boxshot lazyloaded']"))).get_attribute("srcset"))
        product_single_dict["title"] = product_title
        product_single_dict["price"] = product_price
        product_single_dict["status"] = product_status
        product_single_dict["image"] = product_image
        return product_single_dict

    def get_all_data(self):
        self.all_links = web.get_all_product_links()
        product_dict = [{}]
        product_single_dict = {}
        #loop get_one_data with all the data
        product_dict.append(self.get_one_data(self.all_links[0],product_single_dict))
        product_single_dict.clear()
        print(product_dict[0])
        pass

if __name__ == "__main__":
    web = Scraper()
    web.get_all_data()
    pass

