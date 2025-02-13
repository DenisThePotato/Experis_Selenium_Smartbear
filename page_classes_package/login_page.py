from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginPage:
    def __init(self, driver:webdriver):
        self.driver = driver
        self.username = "tester1"
        self.password = "Tester1"


    def page_title_text(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".page-title > h1").text

    def register_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, "a.register-button")
    #//*[@id="content-center"]/div/div/div[2]/article[1]