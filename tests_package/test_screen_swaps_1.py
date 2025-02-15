from unittest import TestCase
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
        # test A
        main_page_text = self.main_page.page_title_text()
        category = self.main_page.get_random_category()
        category_text = category.text
        category.click()
        self.assertEqual(self.category_page.page_title_text(), category_text, "Test A failed- Category title incorrect")
        #self.assertEqual(self.category_page.breadcrumb_title(), category_text, "Test A failed- breadcrumb title incorrect")
        # test B
        self.category_page.show_max_products_per_page()
        product_block = self.category_page.get_random_product_block()
        product_name = self.category_page.product_block_name(product_block)
        self.category_page.click_on_product_block(product_block)
        self.assertEqual(self.product_page.page_title_text(), product_name, "Test B failed- Product title incorrect")
        # test C
        self.product_page.item_category().click()
        self.assertEqual(self.category_page.page_title_text(), category_text, "Test C failed- breadcrumb Back to category page ")
        # test D
        self.category_page.main_page().click()
        self.assertEqual(main_page_text, self.main_page.page_title_text(), "Test D failed- breadcrumb back to main screen")


    """home page -> category page"""
    def test_a(self):
        category = self.main_page.get_random_category()
        category_text = category.text
        category.click()
        self.assertEqual(self.category_page.page_title_text(), category_text)

    """category page -> product page"""
    def test_b(self):
        self.driver.get("https://bearstore-testsite.smartbear.com/watches")
        self.category_page.show_max_products_per_page()
        product_block = self.category_page.get_random_product_block()
        product_name = self.category_page.product_block_name(product_block)
        self.category_page.click_on_product_block(product_block)
        self.assertEqual(self.product_page.page_title_text(), product_name)

    """product page -> category page"""
    def test_c(self):
        self.driver.get("https://bearstore-testsite.smartbear.com/ball-chair")
        self.product_page.item_category().click()
        self.assertEqual(self.category_page.page_title_text(), category_text)

    """category page -> home page"""
    def test_d(self):
        pass

