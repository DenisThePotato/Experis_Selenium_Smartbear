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

class OrderDetailsPage:
    """class representing the order details page"""
    def __init__(self, driver:webdriver):
        self.driver = driver

    def headline_order_number(self) -> str:
        """returns the order number from the headline"""
        return self.driver.find_element(By.CSS_SELECTOR, ".text-muted > small").text

    def order_details_table_order_number(self) -> str:
        """returns the order number from the order information table"""
        table_columns =  self.driver.find_elements(By.CSS_SELECTOR, ".col-6.col-sm-auto.pb-3")
        for i in table_columns:    # goes over table columns and returns the order number from the relevant one.
            if i.find_element(By.XPATH, ".//h5").text == "Order #":
                return i.find_element(By.XPATH, ".//div[1]").text