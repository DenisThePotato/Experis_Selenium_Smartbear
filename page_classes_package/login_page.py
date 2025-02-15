from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint, choice
from time import sleep
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import uniform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class LoginPage:
    def __init(self, driver:webdriver):
        self.driver = driver
        self.username = "tester1"
        self.password = "Tester1"


    def page_title_text(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".page-title > h1").text

    def register_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, "a.register-button")
    #//*[@id="content-center"]/div/div/div[2]/article[1]