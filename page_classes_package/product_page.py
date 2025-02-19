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

class ProductPage:
    """a class giving actions and info for product pages"""
    def __init__(self, driver:webdriver):
        self.driver = driver

    def page_title_text(self) -> str:
        """returns the text of the headline of the page"""
        return self.driver.find_element(By.CLASS_NAME, "pd-name").text

    def item_category(self):
        """returns the category of the item from the breadcrumb UI element.
        can be used to retrieve the items category name or to open its category page"""
        return self.driver.find_elements(By.CSS_SELECTOR, ".breadcrumb.mb-0 > li")[1]

    def breadcrumb_title(self) -> str:
        """returns the item name from the breadcrumb UI element"""
        return self.driver.find_element(By.CSS_SELECTOR, ".breadcrumb-item.active > span").text

    def set_quantity(self, quantity:int) -> None:
        """clears and types a desired amount in the quantity box"""
        quantity_box = self.driver.find_element(By.CSS_SELECTOR, ".form-control.form-control-lg")
        quantity_box.clear()
        quantity_box.send_keys(quantity)
        self.wait_for_quantity_update(quantity)

    def add_to_cart(self) -> None:
        """adds the item to cart"""
        self.driver.find_element(By.LINK_TEXT, "Add to cart").click()

    def increase_quantity_by_one(self) -> None:
        """increases item quantity by one using the '+' button"""
        quantity = self.get_quantity()
        self.driver.find_element(By.CSS_SELECTOR, ".fa.fa-plus").click()
        self.wait_for_quantity_update(quantity + 1)

    def decrease_quantity_by_one(self) -> None:
        """decreases item quantity by one using the '-' button"""
        quantity = self.get_quantity()
        self.driver.find_element(By.CSS_SELECTOR, ".fa.fa-minus").click()
        self.wait_for_quantity_update(quantity - 1)

    def has_short_description(self) -> bool:
        """returns the boolean result of whether the product has a short description under its name"""
        try:
            self.driver.find_element(By.CLASS_NAME, "pd-description")
            return True
        except:
            return False

    def description_text(self) -> str:
        """returns the short description of the item"""
        return self.driver.find_element(By.CLASS_NAME, "pd-description").text

    def block_pricing_dict(self) -> dict:
        """returns the table rows of the quantity and price for block pricing as a dict: {quantity:price}"""
        block_dict = {}
        quantities = self.driver.find_elements(By.CSS_SELECTOR, ".pd-tierprice-qty.text-center")
        prices = self.driver.find_elements(By.CSS_SELECTOR, ".pd-tierprice-price.text-nowrap.text-center")
        for i in range(len(quantities)):
            block_dict[int(quantities[i].text[0])] = Helper.extract_price(prices[i].text)   #quantities[i].text[0] - the second index is +
        return block_dict

    def is_block_priced(self) -> bool:
        """returns a boolean result of whether the product has block pricing or not"""
        try:
            block = self.driver.find_element(By.CLASS_NAME, "pd-tierprices")
            return len(block.find_elements(By.XPATH, './*')) > 0 # checks if the block has children or not
        except:
            return False

    def get_quantity(self) -> int:
        """returns the quantity from the quantity box"""
        return int(self.driver.find_element(By.CSS_SELECTOR, ".form-control.form-control-lg").get_attribute("value"))

    def price_float(self) -> float:
        """returns the float value of the price of the product"""
        full_price_str = self.driver.find_element(By.CSS_SELECTOR, "div[class^='pd-price'] > span").text
        return Helper.extract_price(full_price_str)

    def manually_calculated_price(self) -> float:
        """returns the manually calculated price based on the quantity and price on the product page, taking into account
        whether the product has a price block or not"""
        quantity = self.get_quantity()
        quantity_search = quantity
        if self.is_block_priced():
            block_prices = self.block_pricing_dict()
            while quantity_search > 1:
                if quantity in block_prices.keys():
                    return block_prices[quantity] * quantity
                quantity_search -= 1
        return round(quantity * self.price_float(), 3)

    def manually_calculate_price_for_n_quantity(self, quantity) -> float:
        """returns the manually calculated price of n items taking into account block pricing"""
        quantity_search = quantity
        if self.is_block_priced():   # checks if the more complicated block pricing calculation has to happen
            block_prices = self.block_pricing_dict()
            while quantity_search > 1:
                if quantity in block_prices.keys():
                    return block_prices[quantity] * quantity
                quantity_search -= 1
        return round(quantity * self.price_float(), 3)

    def product_info_dictionary(self) -> dict:
        """returns a dictionary with information about the product - name, quantity, price."""
        return {"name" : self.page_title_text(), "quantity": self.get_quantity(), "price" : self.price_float()}

    def wait_for_quantity_update(self, expected_quantity:int) -> None:
        """waits for the quantity to update"""
        if expected_quantity < 1:
            return
        while self.get_quantity() != expected_quantity:
            continue

    def wait_for_cart_to_update_quantity(self, current_quantity) -> None:
        """waits for the quantity to update"""
        pass
        # WebDriverWait(self.driver, 5).until(
        #     lambda driver:
        #         (By.CSS_SELECTOR, "[data-bind-to='CartItemsCount']").text))
        #
        # WebDriverWait(self.driver, 5).until(lambda driver: self.get_subtotal() != subtotal)



