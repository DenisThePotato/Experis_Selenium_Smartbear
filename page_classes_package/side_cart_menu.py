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


class SideCartMenu:
    def __init__(self, driver:webdriver):
        self.driver = driver

    """opens the side cart menu"""
    def open_side_cart(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, "shopbar-cart")))
        #self.driver.find_element(By.CSS_SELECTOR, "[href='/cart']").click()
        self.driver.find_element(By.ID, "shopbar-cart").click()
        self.wait_for_cart_to_open()
        #sleep(2)

    """gets out of the cart and back to the site"""
    def close_side_cart(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".canvas-blocker.canvas-slidable"))
        )
        self.driver.find_element(By.CSS_SELECTOR, ".canvas-blocker.canvas-slidable").click()
        self.wait_for_cart_to_close()
        # overlay = self.driver.find_element(By.CSS_SELECTOR, "div.page-main.canvas-slidable")
        # ActionChains(self.driver).move_to_element(overlay).click().perform()

    def get_item_blocks_list(self):
        return self.driver.find_elements(By.CLASS_NAME, "offcanvas-cart-item")

    def get_item_name_from_block(self, item):
        return item.find_element(By.CSS_SELECTOR, ".col.col-data > a").text

    def get_item_description_from_block(self, item_block):
        return item_block.find_element(By.CSS_SELECTOR, ".short-desc.text-muted").text

    def get_item_quantity_from_block(self, item_block):
        return int(item_block.find_element(By.ID, "item_EnteredQuantity").get_attribute("value"))

    def set_item_quantity_on_block(self, item_block, desired_amount):
        if self.get_item_quantity_from_block(item_block) == desired_amount:
            return
        subtotal = self.get_subtotal()
        quantity_box = item_block.find_element(By.ID, "item_EnteredQuantity")
        quantity_box.clear()
        quantity_box.send_keys(desired_amount)
        self.wait_for_cart_update(subtotal)

    def increase_item_quantity_by_n(self, item_block, increment):
        if increment < 0:
            return
        subtotal = self.get_subtotal()
        self.set_item_quantity_on_block(item_block, self.get_item_quantity_from_block(item_block) + increment)
        self.wait_for_cart_update(subtotal)

    def decrease_item_quantity_by_n(self, item_block, decrement):
        if self.get_item_quantity_from_block(item_block) - decrement < 1:
            self.set_item_quantity_on_block(item_block, 1)
            return
        self.set_item_quantity_on_block(item_block, self.get_item_quantity_from_block(item_block) - decrement)

    def get_item_price_from_block(self, item_block):
        price_str =  item_block.find_element(By.CSS_SELECTOR, ".price.unit-price").text
        return Helper.extract_price(price_str)

    """removes a specific item from cart"""
    def remove_item(self, item_block):
        item_amount = len(self.get_item_blocks_list())
        if item_amount == 0:
            return
        item_block.find_element(By.CSS_SELECTOR, "[title='Remove']").click()
        WebDriverWait(self.driver, 5).until(lambda driver: len(self.get_item_blocks_list()) == item_amount - 1)

    def get_subtotal(self):
        subtotal = self.driver.find_element(By.CSS_SELECTOR, ".sub-total.price").text
        return Helper.extract_price(subtotal)

    def get_manually_calculated_subtotal(self):
        subtotal = 0
        for i in self.get_item_blocks_list():
            subtotal += self.get_item_quantity_from_block(i) * self.get_item_price_from_block(i)

    def checkout(self):
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-clear").click()

    """empties the cart"""
    def empty_cart(self):
        for i in range (len(self.get_item_blocks_list())):
            self.remove_item(self.get_item_blocks_list()[0])
            #sleep(1)
            #self.wait_for_cart_update(self.get_subtotal())

    def go_to_cart_page(self):
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-success").click()

    def wait_for_cart_update(self, subtotal:float):
        if subtotal == 0:
            return
        WebDriverWait(self.driver, 5).until(lambda driver: self.get_subtotal() != subtotal)

    def wait_for_cart_to_close(self):
        # wait = WebDriverWait(self.driver, 15)
        # wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "canvas-blocking")))
        WebDriverWait(self.driver, 5).until(
            lambda driver: "canvas-slid" not in driver.find_element(By.XPATH, "//body").get_attribute("class"))

    def wait_for_cart_to_open(self):
        # wait = WebDriverWait(self.driver, 5)
        # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "canvas-blocking")))
        WebDriverWait(self.driver, 5).until(
            lambda driver: "canvas-slid" in driver.find_element(By.XPATH, "//body").get_attribute("class"))

    def product_block_dictionary(self, item_block):
        return {
            "name" : self.get_item_name_from_block(item_block),
            "quantity": self.get_item_quantity_from_block(item_block),
            "price" : self.get_item_price_from_block(item_block)
        }

    """get the total price of the product block (not explicitly shown in cart)"""
    def get_total_price_from_block(self, item_block):
        return self.get_item_price_from_block(item_block) * self.get_item_quantity_from_block(item_block)

    """returns a boolean value of whether the side cart is open or not"""
    def is_side_cart_open(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".canvas-blocking.canvas-noscroll.canvas-overlay.canvas-sliding.canvas-sliding-left.canvas-lg.canvas-slid")
        except:
            return False
        return True