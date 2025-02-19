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
    """class representing the login page"""
    def __init__(self, driver:webdriver):
        self.driver = driver

    def page_title_text(self) -> str:
        """returns the page title"""
        return self.driver.find_element(By.TAG_NAME, "h1").text

    def register_button(self) -> None:
        """clicks the register button (-> account creation page)"""
        return self.driver.find_element(By.CSS_SELECTOR, "a.register-button").click()

    def fill_username(self, username) -> None:
        """fill the username box"""
        username_box = self.driver.find_element(By.ID, "UsernameOrEmail")
        username_box.clear()
        username_box.send_keys(username)

    def fill_password(self, password) -> None:
        """fill the password box"""
        password_box = self.driver.find_element(By.ID, "Password")
        password_box.clear()
        password_box.send_keys(password)

    def press_login(self) -> None:
        """click on login"""
        self.driver.find_element(By.CSS_SELECTOR, ".form-group > button").click()

    def logout(self) -> None:
        """open the account dropdown and click logout"""
        # dropdown_element = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-menu.dropdown-menu-right.show > a")
        # dropdown = Select(dropdown_element)
        # dropdown.select_by_visible_text("Log out")
        self.driver.find_element(By.CSS_SELECTOR, "#menubar-my-account > .dropdown").click()
        WebDriverWait(self.driver, 5).until(
            lambda driver: 'shown' in driver.find_element(By.CSS_SELECTOR, '.dropdown-menu.dropdown-menu-right').get_attribute('class'))
        self.driver.find_element(By.LINK_TEXT, "Log out")