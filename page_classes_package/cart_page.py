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

class CartPage:
    def __init__(self, driver:webdriver):
        self.driver = driver

    def open_cart(self):
        #self.driver.find_element(By.CSS_SELECTOR, "[href='/cart']").click()
        self.driver.find_element(By.ID, "shopbar-cart").click()

    def item_list(self):
        self.driver.find_elements(By.CLASS_NAME, "offcanvas-cart-item")

    def item_name(self, item):
        return item.find_element(By.CSS_SELECTOR, ".col.col-data > a").text

    def item_description(self):
        pass

    def item_quantity(self):
        pass

    def item_price(self):
        pass

    def remove_item(self):
        pass

    def total_price(self):
        pass

    def checkout(self):
        pass