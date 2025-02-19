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

from page_classes_package.common_page import Helper

class CartPage:
    """class representing the main cart page"""
    def __init__(self, driver:webdriver):
        self.driver = driver

    def page_title_text(self) -> str:
        """returns the page title string"""
        return self.driver.find_element(By.CLASS_NAME, "h3").text

    def checkout(self) -> None:
        """clicks on checkout"""
        self.driver.find_element(By.ID, "checkout").click()

    def get_subtotal(self) -> float:
        """returns the float"""
        return Helper.extract_price(
            self.driver.find_element(By.CSS_SELECTOR, ".cart-summary-subtotal > .cart-summary-value").text)

    def quantity_element_list(self) -> list:
        """returns all quantity box form control elements (can be changed via number inputs)"""
        return self.driver.find_elements(By.CSS_SELECTOR, "[data-href^='/shoppingcart/updatecart']")

    def cart_row_elements_list(self) -> list:
        """returns the product row elements from the cart"""
        return self.driver.find_elements(By.CLASS_NAME, "cart-row")[1:]

    def increase_all_quantities_by_n(self, increment) -> None:
        """increases all product quantities in the cart by n"""
        for i in range(len(self.quantity_element_list())):
            #current_subtotal = self.get_subtotal()
            current_increment = increment + int(self.quantity_element_list()[i].get_attribute("value"))
            self.quantity_element_list()[i].clear()
            self.quantity_element_list()[i].send_keys(current_increment)
            #self.wait_for_cart_update(current_subtotal)
            sleep(3)

    def get_total_item_price_element_list(self) -> list:
        """returns a list of all total item price elements on the page"""
        return self.driver.find_elements(By.CSS_SELECTOR, "[data-caption='Total'] > .price")

    def wait_for_cart_update(self, subtotal:float) -> None:
        """should wait for the cart to update. but doesnt :) """
        if subtotal == 0:
            return
        WebDriverWait(self.driver, 5).until(lambda driver: self.get_subtotal() != subtotal)