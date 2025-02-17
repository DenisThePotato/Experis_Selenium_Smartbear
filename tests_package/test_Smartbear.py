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

from page_classes_package.cart_page import CartPage
from page_classes_package.main_page import MainPage
from page_classes_package.category_page import CategoryPage
from page_classes_package.order_details_page import OrderDetailsPage
from page_classes_package.product_page import ProductPage
from page_classes_package.side_cart_menu import SideCartMenu
from page_classes_package.login_page import LoginPage
from page_classes_package.checkout_pages import CheckoutPage

class TestSmartbear(TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()
        self.driver.get("https://bearstore-testsite.smartbear.com/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.main_page = MainPage(self.driver)
        self.category_page = CategoryPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_side_page = SideCartMenu(self.driver)
        self.login_page = LoginPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
        self.order_details_page = OrderDetailsPage(self.driver)

    def tearDown(self):
        sleep(3)
        self.driver.quit()

    def test_1_E2E(self):
        # test A- home page -> category page
        main_page_text = self.main_page.page_title_text()
        category = self.main_page.get_random_category()
        category_text = category.text
        category.click()
        self.assertEqual(self.category_page.page_title_text(), category_text, "Test A failed- category title incorrect")
        self.assertEqual(self.category_page.breadcrumb_title(), category_text, "Test A failed- breadcrumb title incorrect")

        # test B- category page -> product page
        self.category_page.show_max_products_per_page()
        product_block = self.category_page.get_random_product_block()
        product_name = self.category_page.product_block_name(product_block)
        self.category_page.click_on_product_block(product_block)
        self.assertEqual(self.product_page.page_title_text(), product_name, "Test B failed- product title incorrect")
        self.assertEqual(self.product_page.breadcrumb_title(), product_name, "Test B failed- breadcrumb title incorrect")

        # test C- product page -> category page
        self.product_page.item_category().click()
        self.assertEqual(self.category_page.page_title_text(), category_text, "Test C failed- page title incorrect")
        self.assertEqual(self.category_page.breadcrumb_title(), category_text,"Test C failed- breadcrumb title incorrect")

        # test D
        self.category_page.main_page().click()
        self.assertEqual(self.main_page.page_title_text(), main_page_text, "Test D failed- page title incorrect")


    """home page -> category page"""
    def test_1_a(self):
        category = self.main_page.get_random_category()
        category_text = category.text
        category.click()
        self.assertEqual(self.category_page.page_title_text(), category_text)

    """category page -> product page"""
    def test_1_b(self):
        self.driver.get("https://bearstore-testsite.smartbear.com/watches")
        self.category_page.show_max_products_per_page()
        product_block = self.category_page.get_random_product_block()
        product_name = self.category_page.product_block_name(product_block)
        self.category_page.click_on_product_block(product_block)
        self.assertEqual(self.product_page.page_title_text(), product_name)

    """product page -> category page"""
    def test_1_c(self):
        self.driver.get("https://bearstore-testsite.smartbear.com/ball-chair")
        self.product_page.item_category().click()

    """category page -> home page"""
    def test_1_d(self):
        pass

    """add 2 products with different quantities, and check the product quantities in cart"""
    def test_2_E2E(self):
        self.cart_side_page.delete_cart()
        products_to_cart = 2
        categories_used_text = []
        for i in range(1, products_to_cart + 1):
            category = self.main_page.get_random_category()
            while category.text in categories_used_text or category.text == "Gift Cards":
                category = self.main_page.get_random_category()
            categories_used_text.append(category.text)
            category.click()
            self.category_page.show_max_products_per_page()
            self.category_page.click_on_product_block(self.category_page.get_random_product_block())
            self.product_page.set_quantity(i + 1)
            self.product_page.add_to_cart()
            self.main_page.open_main_screen()
        # the products are in the cart. now just check the cart.
        self.cart_side_page.open_cart()
        cart_product_blocks = self.cart_side_page.item_blocks_list()
        for i in range(products_to_cart):
            self.assertEqual(self.cart_side_page.item_quantity(cart_product_blocks[i]), (i + 1), "quantity incorrect")

    def test_2_misc(self):
        self.driver.get("https://bearstore-testsite.smartbear.com/ball-chair")
        self.cart_side_page.open_cart()
        sleep(1)
        self.cart_side_page.close_cart()
        self.main_page.open_main_screen()

    def test_8_E2E(self):
        self.assertIn("Your order has been received", self.checkout_page.completion_page_checkout_data())

    def test_9_E2E(self):
        self.main_page.click_login()
        self.login_page.fill_username("tester12345")
        self.login_page.fill_password("Tester12345")
        self.login_page.press_login()
        self.login_page.logout()

    def test_messing_around(self):
        # Locate the element
        self.cart_side_page.open_cart()
        element = self.driver.find_element(By.CSS_SELECTOR, '.canvas-blocking')

        # Execute JavaScript to get the computed style
        display = self.driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');",
                                        element)
        visibility = self.driver.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue('visibility');", element)

        # Print the display and visibility properties
        print(f"Display: {display}")
        print(f"Visibility: {visibility}")

