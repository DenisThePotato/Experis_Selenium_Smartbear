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
    """a helper class containing static methods (for now) to help the page classes with various tasks"""
    def __init__(self, driver:webdriver):
        self.driver = driver


    @staticmethod
    def display_and_visibility_of_element(driver: webdriver, element) -> None:
        """returns the elements visibility and display, to know if wait for visibility can be used"""
        display = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');",
                                        element)   # get the display
        visibility = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue('visibility');", element)   # get the visibility
        print(f"display: {display}")
        print(f"visibility: {visibility}")


    @staticmethod
    def extract_price(price: str) -> float:
        """extracts the relevant price details from a string and returns it as a float"""
        cleaned_price = price.replace("$", "")
        cleaned_price = cleaned_price.replace(",", "")
        cleaned_price = cleaned_price.split()[0]
        return round(float(cleaned_price), 3)