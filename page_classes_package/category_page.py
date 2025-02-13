from selenium import webdriver
from selenium.webdriver.common.by import By

class CategoryPage:
    def __init__(self, driver:webdriver):
        self.driver = driver
    
    def product_list(self):
        #return self.driver.find_elements(By.CSS_SELECTOR, "#artlist-9785039924>article")
        return self.driver.find_elements(By.XPATH, "//div[@id='artist-8431367681']//article[@class='art']")

    def page_title_text(self):
        return self.driver.find_element(By.CLASS_NAME, "h3").text

    def show_120_products_per_page(self):
        self.driver.find_element(By.ID, "artlist-action-pagesize").click()
        self.driver.find_element(By.CSS_SELECTOR, "[value='12']").click()

