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

class ProductPage:
    def __init__(self, driver:webdriver):
        self.driver = driver

    def page_title_text(self):
        return self.driver.find_element(By.CLASS_NAME, "pd-name").text

    def item_category(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".breadcrumb.mb-0 > li")[1]

    def breadcrumb_title(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".breadcrumb-item.active > span").text

    """changes the quantity and adds to cart"""
    def add_to_cart(self, quantity:int):
        for i in range(quantity - 1):
            self.driver.find_element(By.CSS_SELECTOR, "span[class='input-group-btn'] > button[type='button' > i]").click()
        self.driver.find_element(By.LINK_TEXT, "Add to cart").click()

