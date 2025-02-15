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

class CategoryPage:
    def __init__(self, driver:webdriver):
        self.driver = driver

    def sub_categories_list(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".artlist-sub-categories > article")

    def product_list(self):
        # return self.driver.find_elements(By.CSS_SELECTOR, "#artist-8431367681 > article") find only for specific category
        return self.driver.find_elements(By.CSS_SELECTOR, "[id^='artlist-'] > article")

    def get_random_product_block(self):
        return self.product_list()[randint(0, len(self.product_list()) - 1)]

    def click_on_product_block(self, block):
        block.find_element(By.CSS_SELECTOR, "h3 > a > span").click()

    def product_block_name(self, block):
        return block.find_element(By.CSS_SELECTOR, "h3 > a > span").text

    def page_title_text(self):
        return self.driver.find_element(By.CLASS_NAME, "h3").text

    def show_max_products_per_page(self):
        dropdown_element = self.driver.find_element(By.ID, "artlist-action-pagesize")
        dropdown = Select(dropdown_element)
        dropdown.select_by_value(self.max_items_per_page_dropdown_str())

    def items_per_page_dropdown_options_list(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "#artlist-action-pagesize > option")

    def max_items_per_page_dropdown_str(self):
        option_elements = self.items_per_page_dropdown_options_list()
        max_option = -1
        for element in option_elements:
            if int(element.text) > max_option:
                max_option = int(element.text)
        return str(max_option)

    def main_page(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".breadcrumb.mb-0 > li:nth-child(1) > a > i")

    def breadcrumb_title(self):
        return self.driver.find_element(By.CSS_SELECTOR, "breadcrumb-item.active > span").text

