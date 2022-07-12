from argparse import Action
from cgi import print_arguments
from lib2to3.pgen2 import driver
from math import prod
from operator import truediv
import os
from re import M
from turtle import delay
from unicodedata import name
import webbrowser
import uuid
import json
import urllib.request
from pathlib import Path
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

class Scraper:

    def __init__(self) -> webdriver.Chrome():
        self.age_restriction_pass = False
        self.driver = webdriver.Chrome() 
        self.URL = "https://store.eu.square-enix-games.com/en_GB/"
        self.driver.get(self.URL)
        self.delay = 10
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-banner-sdk"]')))
            print("Frame Ready!")
            #driver.switch_to.frame('onetrust-banner-sdk')
            accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            print("Accept Cookies Button Ready!")
            time.sleep(1)
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

        a = ActionChains(self.driver)
        m = self.driver.find_element(By.XPATH,'//li[@id="merchandise"]')
        a.move_to_element(m).perform()
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//li[@id="all-merchandise"]'))).click()
        time.sleep(1)
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
        return list_of_links
    
    def get_game_product(self, list_of_links):
        a = ActionChains(self.driver)
        m = self.driver.find_element(By.XPATH,'//li[@id="games"]')
        a.move_to_element(m).perform()
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//li[@id="all-games"]'))).click()
        time.sleep(1)
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
        return list_of_links
    
    def get_all_product_links(self, list_of_links=[]):
        self.get_game_product(list_of_links)
        self.get_merch_product(list_of_links)
        self.all_links = list_of_links
        return list_of_links

    def get_age_restriction(self):
        self.driver.find_element(By.XPATH, "//select[@data-internal-id='birthday-day']/option[text()='1']").click()
        self.driver.find_element(By.XPATH, "//select[@data-internal-id='birthday-month']/option[text()='January']").click()   
        self.driver.find_element(By.XPATH, "//select[@data-internal-id='birthday-year']/option[text()='2004']").click()
        self.driver.find_element(By.XPATH, "//button[@data-internal-id='save-birthday']").click()
        pass

    def get_one_data(self, one_link):
        #get pass age restriction if there is any
        self.driver.get(one_link)
        self.product_single_dict={}
        if(self.age_restriction_pass == False):
            try:
                self.get_age_restriction()
                self.age_restriction_pass = True
                print("Age Restriction Passed")
            except:
                print("Age Restriction Not Passed")
        try:
            self.driver.find_element(By.XPATH, "//a[@data-target='#product-details']").click()
        except:
            self.driver.find_element(By.XPATH, "//button[@class='btn dropdown-toggle']").click()
            self.driver.find_element(By.XPATH, "//a[@class='dropdown-item']").click()
            one_link = self.driver.current_url
        #get data from the page
        self.product_title = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "product-title"))).get_attribute("textContent"))
        # try:
        #     product_price = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@data-internal-id='product-strike-through']"))).get_attribute("textContent"))
        # except:
        #product_price
        self.product_price = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@data-internal-id='product-price']"))).get_attribute("textContent"))
        #product_status
        self.product_status = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buy_button']"))).text)
        #product_image
        self.product_image = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='boxshot lazyloaded']"))).get_attribute("srcset"))
        self.product_image = self.product_image.replace(" ","").replace("1x","").replace("2x","").split(',')
        
        #product-SKU
        self.product_SKU = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='product-info-details-table table-responsive']/table/tbody/tr[td[contains(.,'SKU')]]/td[2]"))).text)
        
        #Save images into images folder
        base = Path('images')
        base.mkdir(exist_ok=True)
        filename = os.path.join(base, ""+self.product_SKU+".jpg")
        for imglink in self.product_image:
            urllib.request.urlretrieve(imglink,filename)

        self.product_single_dict["title"] = self.product_title
        self.product_single_dict["price"] = self.product_price.replace("\n","")
        self.product_single_dict["status"] = self.product_status
        self.product_single_dict["image"] = self.product_image
        self.product_single_dict["SKU"] = self.product_SKU
        self.product_single_dict["Link"] = one_link
        self.product_single_dict["UUID"] = uuid.uuid4().hex
        return self.product_single_dict

    def get_all_data(self):
        #self.all_links = web.get_all_product_links()
        self.product_dict = []
        #loop get_one_data with all the data
        links = ["https://store.eu.square-enix-games.com/en_GB/product/725931/chrono-cross-the-radical-dreamers-edition-steam","https://store.eu.square-enix-games.com/en_GB/product/564495/final-fantasy-vii-remake-1st-class-edition-ps4"]
        for link in links:
            self.product_single_dict = self.get_one_data(link)
            self.product_dict.append(self.product_single_dict)
        base = Path('raw_data')
        base.mkdir(exist_ok=True)
        with open(base/'data.json','w',encoding='utf-8') as f:
            json.dump(self.product_dict,f,ensure_ascii=False,indent=4)
        
        


if __name__ == "__main__":
    web = Scraper()
    web.get_all_data()
    pass