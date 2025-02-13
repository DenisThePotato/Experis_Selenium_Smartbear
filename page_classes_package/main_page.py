from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By

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
        self.driver.find_element(By.CSS_SELECTOR, "[class='shopbar-col shop-logo']").click()

    def page_title_text(self):
        return self.driver.find_element(By.CLASS_NAME, "h2").text