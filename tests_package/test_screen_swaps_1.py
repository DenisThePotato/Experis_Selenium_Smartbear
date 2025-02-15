from itertools import product
from unittest import TestCase
from random import randint, choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import uniform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from page_classes_package.main_page import MainPage
from page_classes_package.category_page import CategoryPage
from page_classes_package.product_page import ProductPage


class ScreenSwap(TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()
        self.driver.get("https://bearstore-testsite.smartbear.com/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.main_page = MainPage(self.driver)
        self.category_page = CategoryPage(self.driver)
        self.product_page = ProductPage(self.driver)

    def tearDown(self):
        sleep(3)
        self.driver.quit()

    def test_1_E2E(self):
        category = self.main_page.get_random_category()
        category.click()
        self.assertEqual(self.category_page.page_title_text(), category.text)

