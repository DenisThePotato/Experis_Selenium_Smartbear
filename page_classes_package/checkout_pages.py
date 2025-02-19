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
from random import choice


class CheckoutPage:
    """class representing the various checkout pages"""
    def __init__(self, driver:webdriver):
        self.driver = driver

    def cart_page_click_checkout(self) -> None:
        """clicks checkout"""
        self.driver.find_element(By.ID, "checkout").click()

    ####################################################################################################################

    def address_first_name_fill(self, first_name) -> None:
        """fills the first name box"""
        first_name_box = self.driver.find_element(By.ID, "NewAddress_FirstName")
        first_name_box.clear()
        first_name_box.send_keys(first_name)

    def address_last_name_fill(self, last_name) -> None:
        """fills the last name box"""
        last_name_box = self.driver.find_element(By.ID, "NewAddress_LastName")
        last_name_box.clear()
        last_name_box.send_keys(last_name)

    def address_page_bill_to_this_address(self) -> None:
        """clicks on the bill to this address option"""
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-warning.btn-block.select-billing-address-button").click()

    def address_page_ship_to_this_address(self) -> None:
        """clicks on the ship to this address option"""
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-warning.btn-block.select-shipping-address-button").click()

    ####################################################################################################################

    def shipping_page_shipping_options_list(self) -> list:
        """returns all shipping option elements"""
        return self.driver.find_elements(By.CSS_SELECTOR, ".list-group-item.opt-list-item.shipping-option-item")

    def choose_random_shipping_option(self) -> None:
        """clicks on a random shipping option"""
        choice(self.shipping_page_shipping_options_list()).find_element(By.XPATH, ".//div[1]/div[1]/input[1]").click()

    def shipping_page_click_next(self) -> None:
        """clicks next"""
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-warning.btn-lg.shipping-method-next-step-button").click()

    def shipping_option_name(self, shipping_option) -> str:
        """returns the shipping option name"""
        return shipping_option.find_element(By.CLASS_NAME, "opt-name").text

    ####################################################################################################################


    def payment_page_payment_options_list_without_credit(self) -> list:
        """returns all payment option elements excluding credit"""
        no_credit_options = self.driver.find_elements(By.CSS_SELECTOR, ".list-group-item.opt-list-item.payment-method-item")
        return no_credit_options[:len(no_credit_options) - 1]

    def choose_random_payment_options(self) -> None:
        """clicks on a random payment option"""
        choice(self.payment_page_payment_options_list_without_credit()).find_element(By.XPATH, ".//div[1]/div[1]/input[1]").click()

    def payment_page_click_next(self) -> None:
        """clicks next"""
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-warning.btn-lg.payment-method-next-step-button").click()

    def payment_option_name(self, payment_option) -> str:
        """returns the payment option name"""
        return payment_option.find_element(By.CLASS_NAME, "opt-name").text

    ####################################################################################################################


    def confirmation_page_agree_to_terms(self) -> None:
        """checks the agree to terms box"""
        self.driver.find_element(By.ID, "termsofservice").click()

    def confirmation_page_click_confirm(self) -> None:
        """clicks on confirm"""
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-danger.btn-lg.btn-block.btn-buy").click()

    ####################################################################################################################

    def completion_page_checkout_data(self):
        """returns the block containing the order number"""
        return self.driver.find_element(By.CSS_SELECTOR, ".page-body.checkout-data.pt-4")

    def completion_page_order_number(self) -> str:
        """returns the order number extracted from the block with the order number"""
        return self.completion_page_checkout_data().find_element(By.CSS_SELECTOR, "strong").text

    def completion_page_click_order_details(self) -> None:
        """goes to the order details page"""
        self.driver.find_element(By.CSS_SELECTOR, ".pt-3.mb-5 > a.btn-warning").click()

    def completion_page_title(self) -> str:
        """returns the main screen 'title'- the message that the order was received"""
        return self.driver.find_element(By.TAG_NAME, "h1").text