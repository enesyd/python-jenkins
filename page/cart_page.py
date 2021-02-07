from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from base.page_base import BaseClass


class DecathlonsgCartPage:
    """Navigating to checkout page and delete items from cart"""

    CHECKOUT_BUTTON = (By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.btn-block')
    DELETE_ITEM = (By.CSS_SELECTOR, '.remove-from-cart')
    EMPTY_CART = (By.CSS_SELECTOR, '.alert.alert-warning')

    def __init__(self, driver):
        self.driver = driver
        self.methods = BaseClass(self.driver)

    def navigate_to_checkout_page(self):
        """
        Navigates the checkout page then come back to the cart page

        """
        self.methods.wait_for_element(self.CHECKOUT_BUTTON).click()
        self.driver.back()

    def delete_items_from_cart(self):
        """
        Delete all products from cart page

        """
        self.methods.wait_for_element(self.DELETE_ITEM).click()
        try:
            assert self.methods.wait_for_element(self.EMPTY_CART).is_displayed, True
        except TimeoutException:
            self.delete_items_from_cart()

