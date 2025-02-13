from selenium import webdriver
from selenium.webdriver.common.by import By

class CartPage:
    def __init__(self, driver:webdriver):
        self.driver = driver

    def open_cart(self):
        self.driver.find_element(By.CSS_SELECTOR, "[href='/cart']").click()