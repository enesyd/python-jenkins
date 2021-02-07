from selenium import webdriver
from base.page_base import BaseClass
from page.cart_page import DecathlonsgCartPage
from page.category_page import DecathlonsgCategoryPage
from page.login_page import DecathlonsgLogin
from page.main_page import DecathlonsgMain
from page.product_page import DecathlonsgProductPage


class Setup:
    """Selenium initializing requirements are met in here."""

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.methods = BaseClass(self.driver)
        self.decathlonsg_main = DecathlonsgMain(self.driver)
        self.decathlonsg_login = DecathlonsgLogin(self.driver)
        self.decathlonsg_category = DecathlonsgCategoryPage(self.driver)
        self.decathlonsg_product = DecathlonsgProductPage(self.driver)
        self.decathlonsg_cart = DecathlonsgCartPage(self.driver)
