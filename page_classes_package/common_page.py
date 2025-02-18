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

class Helper:
    def __init__(self, driver:webdriver):
        self.driver = driver

    def display_and_visibility_of_element(self):
        self.driver.find_element(By.ID, "shopbar-cart").click()
        # Locate the element
        element = self.driver.find_element(By.CSS_SELECTOR, '.canvas-blocking')
        # Execute JavaScript to get the computed style
        display = self.driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');",
                                        element)
        visibility = self.driver.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue('visibility');", element)
        # Print the display and visibility properties
        print(f"Display: {display}")
        print(f"Visibility: {visibility}")

    """a helper method for other methods. gets a string with a price and returns the float price.
        for example: input = '$2,560.30 USD excl tax.' output = 2560.30"""
    @staticmethod
    def extract_price(price: str):
        cleaned_price = price.replace("$", "")
        cleaned_price = cleaned_price.replace(",", "")
        cleaned_price = cleaned_price.split()[0]
        return round(float(cleaned_price), 3)