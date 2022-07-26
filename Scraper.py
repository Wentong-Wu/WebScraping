from argparse import Action
from cgi import print_arguments
from lib2to3.pgen2 import driver
from math import prod
from operator import truediv
import os
from re import M
from turtle import delay
from typing import Dict
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
        """
        Initialize the webpage and all the atributes
        """
        self.age_restriction_pass = False
        self.driver = webdriver.Chrome() 
        self.URL = "https://store.eu.square-enix-games.com/en_GB/"
        self.driver.get(self.URL)
        self.delay = 10
        pass 

    def accept_cookies(self):
        """
        Accept the cookie appear
        """
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-banner-sdk"]')))
            #driver.switch_to.frame('onetrust-banner-sdk')
            accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            time.sleep(1)
            accept_cookies_button.click()
        except TimeoutException:
            print("Loading took too much time!")
    
    def scroll_to_end(self):
        """
        Scrolls down to the end of the page.
        """
        #Scroll all the way down to get all the products
        length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
        page_end = False
        while(page_end==False):
            last_length_page = length_of_page
            time.sleep(1)
            length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
            if last_length_page==length_of_page:
                page_end=True
    
    def go_to_type_product_page(self,type_of_product):
        """
        Go to a specific type of product page
        """
        a = ActionChains(self.driver)
        m = self.driver.find_element(By.XPATH,'//li[@id="'+type_of_product+'"]')
        a.move_to_element(m).perform()
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//li[@id="all-'+type_of_product+'"]'))).click()
        time.sleep(1)

    def get_product(self,list_of_links = []) -> list:
        """
        Get all the product links in a the page.
        """
        #Gets all the link to the products
        elements = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="product-link-box"]')))
        for elem in elements:
            list_of_links.append(elem.get_attribute('href'))
        return list_of_links

    def get_age_restriction(self):
        """
        This method will be called if the content is blocked by an age restriction.
        This would set the age of the user to 18+ to ensure all the content can be accessed.
        """
        self.driver.find_element(By.XPATH, "//select[@data-internal-id='birthday-day']/option[text()='1']").click()
        self.driver.find_element(By.XPATH, "//select[@data-internal-id='birthday-month']/option[text()='January']").click()   
        self.driver.find_element(By.XPATH, "//select[@data-internal-id='birthday-year']/option[text()='2004']").click()
        self.driver.find_element(By.XPATH, "//button[@data-internal-id='save-birthday']").click()
        pass

    def download_image(self,prod_sku, prod_image):
        """
        Download image into a folder
        """
        #Save images into images folder
        base = Path('images')
        base.mkdir(exist_ok=True)
        filename = os.path.join(base, ""+prod_sku+".jpg")
        for imglink in prod_image:
            urllib.request.urlretrieve(imglink,filename)
        
    def get_one_data(self, one_link) -> dict:
        """
        Get the data from the web and store it into a dictionary then returns it.
        """
        #get pass age restriction if there is any
        self.driver.get(one_link)
        
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
        self.product_single_list=[]
        self.product_single_list.append(WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "product-title"))).get_attribute("textContent"))
        self.product_price_element = WebDriverWait(self.driver, self.delay).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='prices']")))
        self.product_price = self.product_price_element[1].text
        self.product_price = self.product_price.split(" ")
        self.product_single_list.append(self.product_price[0])
        self.product_single_list.append(WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buy_button']"))).text)
        self.product_image = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='boxshot lazyloaded']"))).get_attribute("srcset"))
        self.product_image = self.product_image.replace(" ","").replace("1x","").replace("2x","").split(',')
        self.product_single_list.append(self.product_image)
        self.product_single_list.append(WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='product-info-details-table table-responsive']/table/tbody/tr[td[contains(.,'SKU')]]/td[2]"))).text)
        self.product_single_list.append(one_link)
        self.product_single_list.append(uuid.uuid4().hex)
        self.product_single_list.append(WebDriverWait(self.driver,self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id='breadcrumb']/ol/li[2]"))).get_attribute("textContent"))
        self.download_image(self.product_single_list[4],self.product_single_list[3])
        return self.store_one_data(self.product_single_list)

    def store_one_data(self,single_product_list) -> dict:
        self.product_single_dict = {}
        self.product_single_dict["Title"] = single_product_list[0]
        self.product_single_dict["Price"] = single_product_list[1]
        self.product_single_dict["Status"] = single_product_list[2]
        self.product_single_dict["Image"] = single_product_list[3]
        self.product_single_dict["SKU"] = single_product_list[4]
        self.product_single_dict["Link"] = single_product_list[5]
        self.product_single_dict["UUID"] = single_product_list[6]
        self.product_single_dict["Product_Type"] = single_product_list[7]
        return self.product_single_dict       

    def get_all_product_by_catogary(self, list_catogary):
        """
        Get all the product links on the website.
        """
        self.product = []
        for catogary in list_catogary:
            self.go_to_type_product_page(catogary)
            self.scroll_to_end()
            self.product = self.get_product()
        return self.product

    def download_rawdata(self,product_dict):
        """
        Download the raw data (Dictionary) file as json.
        """
        base = Path('raw_data')
        base.mkdir(exist_ok=True)
        with open(base/'data.json','w',encoding='utf-8') as f:
            json.dump(product_dict,f,ensure_ascii=False,indent=4)

    def get_all_data(self,catogary):
        """
        Get all the data and download it into a folder - Image folder and raw_data folder
        """
        self.accept_cookies()
        self.list_of_catogary = catogary
        self.product_dict = []
        for link in self.get_all_product_by_catogary(self.list_of_catogary):
            self.product_single_dict = self.get_one_data(link)
            self.product_dict.append(self.product_single_dict)
        self.download_rawdata(self.product_dict)

if __name__ == "__main__":
    """
    To ensure that this code only runs if the user is on this script.
    Create a scraper class and runs get_all_data method from the scraper class.
    """
    web = Scraper()
    web.get_all_data(["games","merchandise"])
    pass