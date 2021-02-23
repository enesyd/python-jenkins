from selenium.webdriver.common.by import By
from base.page_base import BaseClass


class DecathlonsgProductPage:
    """DecathlonsgProduct is select exits size, check stock info and add product to cart."""

    ADD_TO_CART_EXISTS = (By.CLASS_NAME, "add")
    NONE_SIZE = (By.CSS_SELECTOR, '//*[@style="display:none"]')
    AVAILABLE_SIZE = (By.CLASS_NAME, 'radio-label')
    ADD_TO_CART = (By.CSS_SELECTOR, '.btn.btn-primary.btn-lg')
    ADD_TO_CART_ICON = (By.CSS_SELECTOR, '.bag-icon')
    CLOSE_POPUP_BTN = (By.ID, 'logo')
    MINIFY_POPUP_BTN = (By.CSS_SELECTOR, '[aria-label="close"]')
    ADDED_TO_CART = (By.CSS_SELECTOR, '.cart_block_no_products.unvisible.empty')
    OUT_OF_STOCK = (By.XPATH, './/*[text()=" There are not enough products in stock "]')
    IFRAME_IS_OPENED = (By.CSS_SELECTOR, '.anchor_right.fb_customer_chat_bounce_in_v2')
    IFRAME = (By.CSS_SELECTOR, '[data-testid="dialog_iframe"]')

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
        Adds product to the cart page and check is it added successfully.

        """
        if self.methods.exist_element(self.ADD_TO_CART_EXISTS):
            try:
                self.driver.execute_script("window.scrollTo(0, 425)")
                self.methods.presence_of_element_located(self.ADD_TO_CART).click()
                assert self.methods.exist_element(self.ADDED_TO_CART), "ADD_TO_CART is not clickable"
            except:
                if self.methods.exist_element(self.IFRAME_IS_OPENED):
                    iframe_name = self.methods.presence_of_element_located(self.IFRAME).get_attribute('name')
                    self.driver.switch_to.frame(iframe_name)
                    self.methods.wait_for_element(DecathlonsgProductPage.CLOSE_POPUP_BTN).click()
                    self.driver.switch_to.default_content()
                    self.methods.wait_for_element(self.ADD_TO_CART_ICON).click()
                else:
                    self.methods.wait_for_element(self.ADD_TO_CART_ICON).click()
        else:
            assert self.methods.wait_for_element(self.ADD_TO_CART_EXISTS).is_displayed(), "No add to cart button"