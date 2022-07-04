from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class Scraper:
        
    def load_and_accept_cookies() -> webdriver.Edge:
        driver = webdriver.Edge() 
        URL = "https://store.eu.square-enix-games.com/en_GB/"
        driver.get(URL)
        delay = 10
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-banner-sdk"]')))
            print("Frame Ready!")
            #driver.switch_to.frame('onetrust-banner-sdk')
            accept_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            print("Accept Cookies Button Ready!")
            accept_cookies_button.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")

        return driver 
pass

web = Scraper
web.load_and_accept_cookies()