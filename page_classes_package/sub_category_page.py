from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep


class SubCategoryPage:
    browser = webdriver.Edge()

    # Go to the required URL
    browser.get("https://bearstore-testsite.smartbear.com/")
    browser.maximize_window()
    browser.implicitly_wait(10)