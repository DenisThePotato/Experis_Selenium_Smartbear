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

class SideCartMenu:
    def __init__(self, driver:webdriver):
        self.driver = driver

    def open_cart(self):
        #self.driver.find_element(By.CSS_SELECTOR, "[href='/cart']").click()
        self.driver.find_element(By.ID, "shopbar-cart").click()
        self.wait_for_cart_to_open()

    """gets out of the cart and back to the site"""
    def close_cart(self):
        self.driver.find_element(By.CSS_SELECTOR, ".canvas-blocker.canvas-slidable").click()
        self.wait_for_cart_to_close()
        # overlay = self.driver.find_element(By.CSS_SELECTOR, "div.page-main.canvas-slidable")
        # ActionChains(self.driver).move_to_element(overlay).click().perform()

    def item_blocks_list(self):
        return self.driver.find_elements(By.CLASS_NAME, "offcanvas-cart-item")

    def item_name(self, item):
        return item.find_element(By.CSS_SELECTOR, ".col.col-data > a").text

    def item_description(self):
        pass

    def item_quantity(self, item):
        return int(item.find_element(By.ID, "item_EnteredQuantity").get_attribute("value"))

    def item_price(self):
        pass

    def remove_item(self):
        item_amount = len(self.item_blocks_list())
        WebDriverWait(self.driver, 5).until(lambda driver: len(self.item_blocks_list()) == item_amount - 1)

    def total_price(self):
        pass

    def checkout(self):
        pass

    def delete_cart(self):
        self.open_cart()
        for i in range(len(self.item_blocks_list())):
            self.item_blocks_list()[i].find_element(By.XPATH, ".//div[2]/div[3]/a[2]").click()
            self.wait_for_cart_update()

    def wait_for_cart_update(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@class="throbber small white" and contains(@style, "opacity: 0")]')))

    def wait_for_cart_to_close(self):
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "canvas-blocking")))

    def wait_for_cart_to_open(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "canvas-blocking")))