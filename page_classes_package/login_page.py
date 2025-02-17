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

class LoginPage:
    def __init__(self, driver:webdriver):
        self.driver = driver

    def page_title_text(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".page-title > h1").text

    def register_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, "a.register-button")
    #//*[@id="content-center"]/div/div/div[2]/article[1]

    def fill_username(self, username):
        username_box = self.driver.find_element(By.ID, "UsernameOrEmail")
        username_box.clear()
        username_box.send_keys(username)

    def fill_password(self, password):
        password_box = self.driver.find_element(By.ID, "Password")
        password_box.clear()
        password_box.send_keys(password)

    def press_login(self):
        self.driver.find_element(By.CSS_SELECTOR, ".form-group > button").click()

    def logout(self):
        # dropdown_element = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-menu.dropdown-menu-right.show > a")
        # dropdown = Select(dropdown_element)
        # dropdown.select_by_visible_text("Log out")
        self.driver.find_element(By.CSS_SELECTOR, "#menubar-my-account > .dropdown").click()
        WebDriverWait(self.driver, 5).until(
            lambda driver: 'shown' in driver.find_element(By.CSS_SELECTOR, '.dropdown-menu.dropdown-menu-right').get_attribute('class'))
        self.driver.find_element(By.LINK_TEXT, "Log out")

    def login_button_logged_in_text(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".menubar-link[href='/customer/info'] > span").text