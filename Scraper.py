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
        """
        This is the init function which runs at the very beginning when the class is called.
        All this does is to open up the webdriver - in my case is Chrome.
        Then it will open up to the URL passed in self.driver.get("URL") - In my case its square enix store
        self.delay is used so that the website waits for the element to appear before executing - 10 second for the driver to find the element.
        """
        self.age_restriction_pass = False
        self.driver = webdriver.Chrome() 
        self.URL = "https://store.eu.square-enix-games.com/en_GB/"
        self.driver.get(self.URL)
        self.delay = 10
        pass 

    def accept_cookies(self):
        """
        This is the accept_cookies method which clicks on the accept button on the cookies.
        try method so that if cookies doesn't exist within the 10 seconds, it will not break the code but instead will execute the except method.
        WebDriverWait - checks to see if a element exists in the html, it passes in a self.delay of 10 second meaning that if it cannot find the element within the 10 seconds, an error will appear.
        Find the accept cookies button element and click it.
        The TimeoutException is when the code couldn't find the element in the webdriverwait, it will replace the error with the block of code in except TimeoutException.
        """
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
    
    def get_product(self,list_of_links,type_of_product):
        """
        This get_product method requires 2 arguments, a list of link and the type of product (such as games/merchandise).
        The type of product argument is used to find the page where all the product exists.
        A list of link argument so that it can append the product into the list and return it to the user.
        First find the where all the type of prodcut is stored and get into that page - In my case there is an nav bar with all the type product can be accessed.
        The while loop is so that it loads all the products in the website since the website loads more product each time you scroll all the way down.
        Finally, append all the product link to the list of link as they are all stored in a specific class. Then return the list of links.
        """
        a = ActionChains(self.driver)
        m = self.driver.find_element(By.XPATH,'//li[@id="'+type_of_product+'"]')
        a.move_to_element(m).perform()
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//li[@id="all-'+type_of_product+'"]'))).click()
        time.sleep(1)
        #Scroll all the way down to get all the products
        length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
        page_end = False
        while(page_end==False):
            last_length_page = length_of_page
            time.sleep(1)
            length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
            if last_length_page==length_of_page:
                page_end=True

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

    def get_one_data(self, one_link):
        """
        This method extracts the data and information required. It requires a argument (a link) to load the locatino of the product.
        First create an empty dictionary to store all the data and information aquried.
        Attempts to run age restriction method to check if the content has an age restriction.
        It will run it until it successfully found a content with age restriction and after that, the web site should save the data and allow the user to access all content which means the age restrcion method will not be required to run, this is to save speed and process of scraping the data.
        After passing the age restriction, it will collect all the useful data and information and store it into the empty dictionary created.
        Download all the product_image and store it into an image folder using urllib.request.urlretrieve.
        Finally, return the dictionary to the user.
        """
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
        self.product_title = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "product-title"))).get_attribute("textContent"))
        self.product_price_element = WebDriverWait(self.driver, self.delay).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='prices']")))
        self.product_price = self.product_price_element[1].text
        self.product_price = self.product_price.split(" ")
        print(self.product_price[0])
        self.product_status = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buy_button']"))).text)
        self.product_image = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='boxshot lazyloaded']"))).get_attribute("srcset"))
        self.product_image = self.product_image.replace(" ","").replace("1x","").replace("2x","").split(',')
        self.product_SKU = (WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='product-info-details-table table-responsive']/table/tbody/tr[td[contains(.,'SKU')]]/td[2]"))).text)
        #Save images into images folder
        base = Path('images')
        base.mkdir(exist_ok=True)
        filename = os.path.join(base, ""+self.product_SKU+".jpg")
        for imglink in self.product_image:
            urllib.request.urlretrieve(imglink,filename)
        self.product_single_dict["title"] = self.product_title
        self.product_single_dict["price"] = self.product_price[0]
        self.product_single_dict["status"] = self.product_status
        self.product_single_dict["image"] = self.product_image
        self.product_single_dict["SKU"] = self.product_SKU
        self.product_single_dict["Link"] = one_link
        self.product_single_dict["UUID"] = uuid.uuid4().hex
        return self.product_single_dict

    def get_all_data(self):
        """
        This method is used to collect all the data and save the data into folder (raw data into json). This uses all the method created.
        First calls the accept_cookies method to by pass the cookies to access all the html content.
        Then collect all the game product links and game merch links using the get_product method.
        Create an empty array named product_dict to store all the dicionary as a list.
        Loop through all the link collected and call get_one_data passing in the link as arugment and then append all the data into the product_dict array.
        All the data should then be stored inside the product_dict array.
        Finally, use json.dump to store all the data into a json file.
        """
        self.all_links = self.get_all_product_links()
        self.accept_cookies()
        self.game_product = []
        self.game_product = self.get_product(self.game_product,"games")
        self.merch_product = []
        self.merch_product = self.get_product(self.merch_product,"merchandise")
        self.product_dict = []
        
        #loop get_one_data with all the data
        #links = ["https://store.eu.square-enix-games.com/en_GB/product/725931/chrono-cross-the-radical-dreamers-edition-steam","https://store.eu.square-enix-games.com/en_GB/product/564495/final-fantasy-vii-remake-1st-class-edition-ps4"]
        for link in self.game_product:
            self.product_single_dict = self.get_one_data(link)
            self.product_single_dict["Game or Merchandise"] = "Game"
            self.product_dict.append(self.product_single_dict)
        for link in self.merch_product:
            self.product_single_dict = self.get_one_data(link)
            self.product_single_dict["Game or Merchandise"] = "Merchandise"
            self.product_dict.append(self.product_single_dict)
        base = Path('raw_data')
        base.mkdir(exist_ok=True)
        with open(base/'data.json','w',encoding='utf-8') as f:
            json.dump(self.product_dict,f,ensure_ascii=False,indent=4)

if __name__ == "__main__":
    """
    To ensure that this code only runs if the user is on this script.
    Create a scraper class and runs get_all_data method from the scraper class.
    """
    web = Scraper()
    web.get_all_data()
    pass