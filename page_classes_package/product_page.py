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

"""a class giving actions and info for product pages"""
class ProductPage:
    def __init__(self, driver:webdriver):
        self.driver = driver

    """returns the text of the headline of the page"""
    def page_title_text(self):
        return self.driver.find_element(By.CLASS_NAME, "pd-name").text

    """returns the category of the item from the breadcrumb UI element.
    can be used to retrieve the items category name or to open its category page"""
    def item_category(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".breadcrumb.mb-0 > li")[1]

    """returns the item name from the breadcrumb UI element"""
    def breadcrumb_title(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".breadcrumb-item.active > span").text

    """clears and types a desired amount in the quantity box"""
    def set_quantity(self, quantity:int):
        quantity_box = self.driver.find_element(By.CSS_SELECTOR, ".form-control.form-control-lg")
        quantity_box.clear()
        quantity_box.send_keys(quantity)

    """adds the item to cart"""
    def add_to_cart(self):
        self.driver.find_element(By.LINK_TEXT, "Add to cart").click()

    """increases item quantity by one using the '+' button"""
    def increase_quantity_by_one(self):
        self.driver.find_element(By.CSS_SELECTOR, ".fa.fa-plus").click()

    """decreases item quantity by one using the '-' button"""
    def decrease_quantity_by_one(self):
        self.driver.find_element(By.CSS_SELECTOR, ".fa.fa-minus").click()

    """returns the boolean result of whether the product has a short description under its name"""
    def has_short_description(self):
        try:
            self.driver.find_element(By.CLASS_NAME, "pd-description")
            return True
        except:
            return False

    """returns the short description of the item"""
    def description_text(self):
        return self.driver.find_element(By.CLASS_NAME, "pd-description").text

    """returns the table rows of the quantity and price for block pricing"""
    def block_pricing_dict(self):
        block_dict = {}
        quantities = self.driver.find_elements(By.CSS_SELECTOR, ".pd-tierprice-qty.text-center")
        prices = self.driver.find_elements(By.CSS_SELECTOR, ".pd-tierprice-price.text-nowrap.text-center")
        for i in range(len(quantities)):
            block_dict[int(quantities[i].text[0])] = float(self.extract_price(prices[i].text)) # prices[i].text[1:]
        return block_dict

    """returns a boolean result of whether the product has block pricing or not"""
    def is_block_priced(self):
        try:
            block = self.driver.find_element(By.CLASS_NAME, "pd-tierprices")
            return len(block.find_elements(By.XPATH, './*')) > 0 # checks if the block has children or not
        except:
            return False

    """returns the float value of the price of the product"""
    def price_float(self):
        full_price_str = self.driver.find_element(By.CSS_SELECTOR, "div[class='pd-price'] > meta[itemprop='price']").get_attribute("content")
        return self.extract_price(full_price_str)
        # cleaned_price = full_price_str.replace("$", "")
        # cleaned_price = cleaned_price.replace(",", "")
        # cleaned_price = cleaned_price.split()[0]
        # return float(cleaned_price)

    """returns the manually calculated price based on the quantity and price on the product page, taking into account
    whether the product has a price block or not"""
    def manually_calculated_price(self):
        quantity = int(self.driver.find_element(By.CSS_SELECTOR,".form-control.form-control-lg").get_attribute("value"))
        quantity_search = quantity
        if self.is_block_priced():
            block_prices = self.block_pricing_dict()
            while quantity_search > 1:
                if quantity in block_prices.keys():
                    return block_prices[quantity] * quantity
                quantity_search -= 1
        return quantity * self.price_float()

    """a helper method for other methods. gets a string with a price and returns the float price.
    for example: input = '$2,560.30 USD excl tax.' output = 2560.30"""
    def extract_price(self, price:str):
        cleaned_price = price.replace("$", "")
        cleaned_price = cleaned_price.replace(",", "")
        cleaned_price = cleaned_price.split()[0]
        return float(cleaned_price)



