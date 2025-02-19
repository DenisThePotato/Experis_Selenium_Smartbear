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
    """class representing the main page"""
    def __init__(self, driver:webdriver):
        self.driver = driver

    def wait_for_main_page(self) -> None:
        """wait for the main page to load properly, doesnt work :) """
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "h2"))
        )

    def category_list(self) -> list:
        """returns the list of categories"""
        return self.driver.find_elements(By.CSS_SELECTOR, "#menu-main > li")

    def get_random_category(self):
        """returns a category not including gift cards"""
        return self.category_list()[randint(0, len(self.category_list()) - 1)]

    def click_login(self) -> None:
        """clicks on login"""
        self.driver.find_element(By.LINK_TEXT, "LOG IN").click()

    def open_main_screen(self) -> None:
        """opens the main screen"""
        self.driver.find_element(By.CSS_SELECTOR, "[title='SmartStore']").click()

    def page_title_text(self) -> str:
        """returns the page title"""
        return self.driver.find_element(By.CLASS_NAME, "h2").text

    def login_button_logged_in_text(self) -> str:
        """returns the username from the user actions dropdown menu title"""
        return self.driver.find_element(By.CSS_SELECTOR, ".menubar-link[href='/customer/info'] > span").text

    def is_logged_in(self) -> bool:
        """returns the boolean result of whether the user is logged in"""
        try:
            self.driver.find_element(By.LINK_TEXT, "LOG IN")
        except:
            return True
        return False