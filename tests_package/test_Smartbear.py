from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import randint, choice, uniform
import logging

from page_classes_package.cart_page import CartPage
from page_classes_package.common_page import Helper
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
        self.main_page.wait_for_main_page()
        sleep(1)
        if self.main_page.is_logged_in():
            self.login_page.logout()
            sleep(1)
        self.cart_side_page.open_side_cart()
        self.cart_side_page.empty_cart()
        self.cart_side_page.close_side_cart()

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
        num_of_products_to_add = 2    # max 5
        expected_product_amounts = [num_of_products_to_add - i for i in range(num_of_products_to_add)]
        categories_used_text = []
        for i in range(num_of_products_to_add):    # add the random products from unique categories to cart
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
        # compare the amount of items in cart to the amounts added
        self.cart_side_page.open_side_cart()
        cart_product_blocks = self.cart_side_page.get_item_blocks_list()
        for i in range(num_of_products_to_add):
            self.assertEqual(self.cart_side_page.get_item_quantity_from_block(cart_product_blocks[i]), expected_product_amounts[i], f"i = {i}, quantity incorrect")

    """NAME - AMOUNT - PRICE
    doesnt work because the price is sometimes taken before the update to the quantity, not taking block price into account"""
    def test_3_E2E(self):
        num_of_products_to_add = 3  # max 5
        products_added_dictionaries = []
        categories_used_text = []
        for i in range(num_of_products_to_add):  # add the random products from unique categories to cart
            category = self.main_page.get_random_category()
            while category.text in categories_used_text or category.text == "Gift Cards":
                category = self.main_page.get_random_category()
            categories_used_text.append(category.text)
            category.click()
            self.category_page.show_max_products_per_page()
            self.category_page.click_on_product_block(self.category_page.get_random_product_block())
            self.product_page.set_quantity(i + 1)
            sleep(1)
            products_added_dictionaries.insert(0, self.product_page.product_info_dictionary())
            self.product_page.add_to_cart()
            self.main_page.open_main_screen()
        self.cart_side_page.open_side_cart()
        for i in range(num_of_products_to_add):
            current_cart_item_dic = self.cart_side_page.product_block_dictionary(self.cart_side_page.get_item_blocks_list()[i])
            for key in products_added_dictionaries[i]:
                self.assertEqual(current_cart_item_dic[key], products_added_dictionaries[i][key], f"{current_cart_item_dic[key]} != {products_added_dictionaries[i][key]}"
                                                                                                  f"\ncurrent item dic: {current_cart_item_dic}\nproducts_added dic: {products_added_dictionaries[i]}")

    """adds 2 random products, removes one and checks the other in the cart (price, name, quantity)"""
    def test_4_E2E(self):
        num_of_products_to_add = 2  # max 5
        categories_used_text = []
        for i in range(num_of_products_to_add):  # add the random products from unique categories to cart
            category = self.main_page.get_random_category()
            while category.text in categories_used_text or category.text == "Gift Cards":
                category = self.main_page.get_random_category()
            categories_used_text.append(category.text)
            category.click()
            self.category_page.show_max_products_per_page()
            self.category_page.click_on_product_block(self.category_page.get_random_product_block())
            self.product_page.set_quantity(i + 1)
            sleep(1)
            self.product_page.add_to_cart()
            if i == 0:
                product_dict = self.product_page.product_info_dictionary()
            self.main_page.open_main_screen()
        self.cart_side_page.open_side_cart()
        self.cart_side_page.remove_item(self.cart_side_page.get_item_blocks_list()[0])   # removes the last item added
        self.assertEqual(self.cart_side_page.product_block_dictionary(self.cart_side_page.get_item_blocks_list()[0]),
                         product_dict, f"cart item dict: {self.cart_side_page.product_block_dictionary(self.cart_side_page.get_item_blocks_list()[0])}"
                                       f"\nproduct page dict: {product_dict}")

    def test_5_E2E(self):
        category = self.main_page.get_random_category()
        while category.text == "Gift Cards":
            category = self.main_page.get_random_category()
        category.click()
        self.category_page.show_max_products_per_page()
        self.category_page.click_on_product_block(self.category_page.get_random_product_block())
        self.product_page.add_to_cart()
        self.assertTrue(self.cart_side_page.is_side_cart_open(),
                        "cart was not opened upon addition of item to cart")
        self.cart_side_page.close_side_cart()
        self.assertFalse(self.cart_side_page.is_side_cart_open(),
                         "cart was not closed when pressing on the side of the screen")
        self.cart_side_page.open_side_cart()
        self.assertTrue(self.cart_side_page.is_side_cart_open(),
                        "cart was not opened upon clicking the cart icon")
        sleep(1)
        self.cart_side_page.go_to_cart_page()
        sleep(1)
        self.assertEqual(self.cart_page.page_title_text(), "Shopping cart",
                         "didnt open the shopping cart page")

    def test_6_E2E(self):
        # product_total_prices = []
        # product_total_quantities = []
        logging.basicConfig(level=logging.INFO)
        total_calculated_cost = 0
        categories_used_text = []
        iterations = 3
        for i in range(iterations):
            category = self.main_page.get_random_category()
            while category.text in categories_used_text or category.text == "Gift Cards":
                category = self.main_page.get_random_category()
            categories_used_text.append(category.text)
            category.click()
            self.category_page.show_max_products_per_page()
            self.category_page.click_on_product_block(self.category_page.get_random_product_block())
            self.product_page.set_quantity(i + 1)
            sleep(2)
            total_calculated_cost += self.product_page.manually_calculated_price()
            # product_total_quantities.insert(0, self.product_page.get_quantity())
            # product_total_prices.insert(0, self.product_page.manually_calculated_price())
            self.product_page.add_to_cart()
            sleep(1)
            if i != iterations - 1:
                self.cart_side_page.close_side_cart()
                sleep(1)
                self.main_page.open_main_screen()
        self.assertEqual(self.cart_side_page.get_subtotal(), total_calculated_cost,
                         "total cost in side cart doesnt match")
        for i in range(iterations):
            logging.info(self.cart_side_page.product_block_dictionary(self.cart_side_page.get_item_blocks_list()[i]))
        self.cart_side_page.go_to_cart_page()
        sleep(1)
        self.assertEqual(self.cart_page.get_subtotal(), total_calculated_cost, "total cost in cart doesnt match")
        # for i in range(iterations):
        #     self.assertEqual(self.cart_side_page.get_item_quantity_from_block(self.cart_side_page.get_item_blocks_list()[i]), product_total_quantities[i],
        #                      "the quantities dont match")
        #     self.assertEqual(self.cart_side_page.get_total_price_from_block(self.cart_side_page.get_item_blocks_list()[i]), product_total_prices),
        #     "item prices dont match"

    def test_7_E2E(self):
        amount_price_tuples_list = []
        categories_used_text = []
        iterations = 2
        for i in range(iterations):
            category = self.main_page.get_random_category()
            while category.text in categories_used_text or category.text == "Gift Cards":
                category = self.main_page.get_random_category()
            categories_used_text.append(category.text)
            category.click()
            self.category_page.show_max_products_per_page()
            self.category_page.click_on_product_block(self.category_page.get_random_product_block())
            self.product_page.set_quantity(i + 1)
            sleep(2)
            amount_price_tuples_list.insert(0, (i + 2, self.product_page.manually_calculate_price_for_n_quantity(i + 2) / (i + 2)))
            # product_total_quantities.insert(0, self.product_page.get_quantity())
            # product_total_prices.insert(0, self.product_page.manually_calculated_price())
            self.product_page.add_to_cart()
            sleep(2)
            if i != iterations - 1:
                self.cart_side_page.close_side_cart()
                sleep(2)
                self.main_page.open_main_screen()
        total_cost = 0
        for i in amount_price_tuples_list:
            total_cost += round(i[0] * i[1], 3)
        self.cart_side_page.go_to_cart_page()
        sleep(2)
        self.cart_page.increase_all_quantities_by_n(1)
        sleep(2)
        for i in range(len(amount_price_tuples_list)):
            self.assertEqual(Helper.extract_price(self.cart_page.get_total_item_price_element_list()[i].text), round(amount_price_tuples_list[i][0]*amount_price_tuples_list[i][1], 3),
                             f"the total item price is not correct {amount_price_tuples_list}")
        self.assertEqual(self.cart_page.get_subtotal(), total_cost,
                         "total cost in side cart doesnt match")
        self.main_page.open_main_screen()
        self.cart_side_page.open_side_cart()
        self.assertEqual(self.cart_side_page.get_subtotal(), total_cost,
                         "the total cost in the side cart is incorrect")



    def test_8_E2E(self):
        username = "tester12345"
        password = "Tester12345"
        iterations = 2
        for i in range(iterations):
            category = self.main_page.get_random_category()
            while category.text == "Gift Cards":
                category = self.main_page.get_random_category()
            category.click()
            self.category_page.show_max_products_per_page()
            self.category_page.click_on_product_block(self.category_page.get_random_product_block())
            self.product_page.set_quantity(i + 1)
            self.product_page.add_to_cart()
            sleep(1)
            if i != iterations - 1:
                self.cart_side_page.close_side_cart()
                sleep(1)
                self.main_page.open_main_screen()
        self.cart_side_page.go_to_cart_page()
        self.cart_page.checkout()
        self.login_page.fill_username(username)
        self.login_page.fill_password(password)
        self.login_page.press_login()
        sleep(1)
        self.cart_page.checkout()
        self.checkout_page.address_page_bill_to_this_address()
        self.checkout_page.address_page_ship_to_this_address()
        self.checkout_page.choose_random_shipping_option()
        self.checkout_page.shipping_page_click_next()
        self.checkout_page.choose_random_payment_options()
        self.checkout_page.payment_page_click_next()
        sleep(1)
        self.checkout_page.confirmation_page_agree_to_terms()
        self.checkout_page.confirmation_page_click_confirm()
        sleep(1)
        self.assertEqual(self.checkout_page.completion_page_title(), "Your order has been received",
                         "no confirmation message")
        completion_page_order_number = self.checkout_page.completion_page_order_number()
        # probably create relevant variables for each class and have them updated on certain method calls
        self.checkout_page.completion_page_click_order_details()
        sleep(1)
        self.assertEqual(self.order_details_page.order_details_table_order_number(), completion_page_order_number,
                         "order number doesnt match order details page table order number")
        self.assertEqual(self.order_details_page.headline_order_number(), completion_page_order_number,
                         "order number doesnt match order details page headline order number")

    # test fails because the login displays the username in all caps. if it doesnt matter- .lower
    def test_9_E2E(self):
        username = "tester12345"
        password = "Tester12345"
        self.main_page.click_login()
        self.login_page.fill_username(username)
        self.login_page.fill_password(password)
        self.login_page.press_login()
        sleep(1)
        self.assertEqual(self.main_page.login_button_logged_in_text(), username, "username doesnt match text")
        self.login_page.logout()
        self.assertFalse(self.main_page.is_logged_in(), "didnt log out properly")

    ####################################################################################################################
    def test_cart_actions(self):
        # random product addition to cart
        iterations = 1
        for i in range(iterations):
            category = self.main_page.get_random_category()
            while category.text == "Gift Cards":
                category = self.main_page.get_random_category()
            category.click()
            self.category_page.show_max_products_per_page()
            self.category_page.click_on_product_block(self.category_page.get_random_product_block())
            self.product_page.set_quantity(i + 1)
            self.product_page.add_to_cart()
            print(self.cart_side_page.get_item_quantity_from_block(self.cart_side_page.get_item_blocks_list()[0]))
            sleep(1)
            if i != iterations - 1:
                self.cart_side_page.close_side_cart()
                sleep(1)
                self.main_page.open_main_screen()
        # in the cart
        # item_block_list = self.cart_side_page.item_blocks_list()
        # self.cart_side_page.remove_item(item_block_list[0])
        sleep(1)
        self.cart_side_page.go_to_cart_page()

    def test_cart_opening(self):
        sleep(1)
        self.cart_side_page.open_side_cart()