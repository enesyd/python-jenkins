from selenium.webdriver.common.by import By
from time import sleep
from base.page_base import BaseClass


class DecathlonsgLogin:
    """Website login page to user logged in."""

    email = 'jugo@getnada.com'
    password = 'test1234'
    EMAIL = (By.NAME, 'email')
    PASSWORD = (By.NAME, 'password')
    NEXT_BUTTON = (By.ID, "next-btn")

    def __init__(self, driver):
        self.driver = driver
        self.methods = BaseClass(self.driver)

    def login(self):
        """
        Fills login informations

        """
        sleep(2)
        self.methods.wait_for_element(self.EMAIL).send_keys(self.email)
        self.methods.wait_for_element(self.NEXT_BUTTON).click()
        self.methods.wait_for_element(self.PASSWORD).send_keys(self.password)
        self.methods.wait_for_element(self.NEXT_BUTTON).click()
