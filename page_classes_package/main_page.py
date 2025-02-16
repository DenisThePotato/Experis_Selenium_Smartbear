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

class MainPage:
    def __init__(self, driver:webdriver):
        self.driver = driver

    def category_list(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "#menu-main > li")

    def get_random_category(self):
        return self.category_list()[randint(0, len(self.category_list()) - 1)]

    def click_login(self):
        self.driver.find_element(By.LINK_TEXT, "LOG IN").click()

    def open_main_screen(self):
        self.driver.find_element(By.CSS_SELECTOR, "[title='SmartStore']").click()

    def page_title_text(self):
        return self.driver.find_element(By.CLASS_NAME, "h2").text