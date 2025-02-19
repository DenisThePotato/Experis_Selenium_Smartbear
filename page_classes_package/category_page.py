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
    """class representing the category page"""
    def __init__(self, driver:webdriver):
        self.driver = driver

    def sub_categories_list(self) -> list:
        """returns a list of the sub categories on the page"""
        return self.driver.find_elements(By.CSS_SELECTOR, ".artlist-sub-categories > article")

    def product_list(self) -> list:
        """returns a list of the products on the page"""
        return self.driver.find_elements(By.CSS_SELECTOR, "[id^='artlist-'] > article")

    def get_random_product_block(self):
        """returns a random product block from the products on the page"""
        return self.product_list()[randint(0, len(self.product_list()) - 1)]

    def click_on_product_block(self, block) -> None:
        """gets a block from params and clicks on it"""
        block.find_element(By.CSS_SELECTOR, "h3 > a > span").click()

    def product_block_name(self, block) -> str:
        """returns the name from the product block"""
        return block.find_element(By.CSS_SELECTOR, "h3 > a > span").text

    def page_title_text(self) -> str:
        """returns the title of the page (category name)"""
        return self.driver.find_element(By.CLASS_NAME, "h3").text

    def show_max_products_per_page(self) -> None:
        """shows the maximum amount of elements visible on the page"""
        dropdown_element = self.driver.find_element(By.ID, "artlist-action-pagesize")
        dropdown = Select(dropdown_element)
        dropdown.select_by_value(self.max_items_per_page_dropdown_str())

    def items_per_page_dropdown_options_list(self) -> list:
        """returns the list of option on the items per page dropdown element"""
        return self.driver.find_elements(By.CSS_SELECTOR, "#artlist-action-pagesize > option")

    def max_items_per_page_dropdown_str(self) -> str:
        """returns the maximal amount of products per page that is able to be shown (from the per page dropdown)"""
        option_elements = self.items_per_page_dropdown_options_list()
        max_option = int(option_elements[0].text)
        #max_option = -1
        for element in option_elements:   # could create a list with [str(i) for i in option_elements] and use max
            if int(element.text) > max_option:
                max_option = int(element.text)
        return str(max_option)

    def go_to_main_page(self) -> None:
        """goes to the home page from the home breadcrumb element"""
        return self.driver.find_element(By.CSS_SELECTOR, ".breadcrumb.mb-0 > li:nth-child(1) > a > i").click()

    def breadcrumb_title(self) -> str:
        """returns the title of the category from the breadcrumb menu"""
        return self.driver.find_element(By.CSS_SELECTOR, ".breadcrumb-item.active > span").text

