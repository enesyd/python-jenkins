from selenium.webdriver.common.by import By
from base.page_base import BaseClass


class DecathlonsgProductPage:
    """DecathlonsgProduct is select exits size, check stock info and add product to cart."""

    NONE_SIZE = (By.CSS_SELECTOR, '//*[@style="display:none"]')
    AVAILABLE_SIZE = (By.CLASS_NAME, 'radio-label')
    ADD_TO_CART = (By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.add-to-cart')
    ADDED_TO_CART = (By.CSS_SELECTOR, '.cart_block_no_products.unvisible.empty')
    OUT_OF_STOCK = (By.XPATH, './/*[text()=" There are not enough products in stock "]')

    def __init__(self, driver):
        self.driver = driver
        self.methods = BaseClass(self.driver)

    def select_size(self):
        """
        Selects product size

        """
        if self.methods.exist_element(self.NONE_SIZE):
            self.methods.wait_for_element(self.AVAILABLE_SIZE).click()

    def check_stock_info(self):
        """
        Search for stock info if the product is not in stock returns False

        """
        if self.methods.exist_element(self.OUT_OF_STOCK):
            return False
        else:
            return True

    def add_product_to_cart(self):
        """
        Adds product to the cart page and check is it added successfully

        """
        self.methods.wait_for_element(self.ADD_TO_CART).click()
        successfully_added = self.methods.exist_element(self.ADDED_TO_CART)
        assert successfully_added, True
