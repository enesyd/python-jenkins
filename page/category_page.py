from time import sleep
from selenium.webdriver.common.by import By
from base.page_base import BaseClass


class DecathlonsgCategoryPage:
    """DecathlonsgCategory is selecting random product from category page ."""

    PRODUCT_CONTAINER = (By.ID, 'products')
    PRODUCT_LIST = (By.CSS_SELECTOR, '.thumbnail.product-thumbnail')

    def __init__(self, driver):
        self.driver = driver
        self.methods = BaseClass(self.driver)

    def selects_random_product(self):
        """
        Select random products from product list.

        """
        sleep(2)
        self.methods.wait_for_element(self.PRODUCT_CONTAINER)
        self.methods.exist_element(self.PRODUCT_LIST, multiple=True)
        products = self.driver.find_elements(*self.PRODUCT_LIST)
        if len(products) > 7:
            random_int = self.methods.random_number(1, 6)
            random_product_url = products[random_int].get_attribute('href')
            random_product_url = random_product_url.split('html')
            random_product_url = random_product_url[0] + 'html'
            self.driver.get(random_product_url)

        else:
            random_int = self.methods.random_number(1, len(products) - 1)
            random_product_url = products[random_int].get_attribute('href')
            random_product_url = random_product_url.split('html')
            random_product_url = random_product_url[0] + 'html'
            self.driver.get(random_product_url)
