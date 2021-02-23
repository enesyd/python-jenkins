from selenium.webdriver.common.by import By
from time import sleep
from base.page_base import BaseClass


class DecathlonsgMain:
    """DecathlonsgMain class lands in the website and it has all the navigation functions."""

    website = 'https://www.decathlon.sg/'
    HOMEPAGE_CONTROL = (By.CSS_SELECTOR, '.elementor-container.elementor-column-gap-default')
    LOGIN_HEADER = (By.CSS_SELECTOR, '#header-user-btn')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.elementor-button-text')
    MAIN_CATS_CONTAINER_HEADER = (By.XPATH, '//*[contains(@class, "cbp-has-submeu")]')
    SUB_CATS_CONTAINER_HEADER = (By.XPATH, '//*[contains(@class, "cbp-category-title")]')
    CART_HEADER = (By.ID, 'button_cart_cart')

    def __init__(self, driver):
        self.driver = driver
        self.methods = BaseClass(self.driver)

    def navigate_to_home_page(self):
        """
        Navigates to the homepage and checks it

        """
        self.driver.get(self.website)
        home_page_loaded = self.methods.exist_element(self.HOMEPAGE_CONTROL)
        assert home_page_loaded, True

    def navigate_to_login_page(self):
        """
        Navigates to the login page

        """
        sleep(2)
        self.methods.hover_element(self.LOGIN_HEADER)
        self.methods.wait_for_element(self.LOGIN_BUTTON).click()

    def navigate_to_random_category_page(self):
        """
        Navigates to a random category page

        """
        self.methods.exist_element(self.SUB_CATS_CONTAINER_HEADER, multiple=True)
        main_categories = self.driver.find_elements(*self.MAIN_CATS_CONTAINER_HEADER)
        sub_categories = self.driver.find_elements(*self.SUB_CATS_CONTAINER_HEADER)
        self.methods.select_random_category(sub_categories, main_categories)

    def navigate_to_cart_page(self):
        """
        Navigates to the cart page.

        if self.methods.exist_element(DecathlonsgProductPage.IFRAME_IS_OPENED):
            iframe_name = self.methods.presence_of_element_located(self.IFRAME).get_attribute('name')
            self.driver.switch_to.frame(iframe_name)
            self.methods.wait_for_element(DecathlonsgProductPage.CLOSE_POPUP_BTN).click()
            self.driver.switch_to.default_content()
            self.methods.wait_for_element(self.CART_HEADER).click()
        else:
            self.methods.wait_for_element(self.CART_HEADER).click()
        """
        self.driver.get("https://www.decathlon.sg/cart")