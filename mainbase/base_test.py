import logging
import unittest
import time  # This import used by test cases don't remove

from mainbase.utils.pytest_marks import Priority, RunOnly, Owner
from mainbase.utils.report_html import decorator_loader, error_logger
from mainbase.utils.settings import Settings, SettingKeys
from mainbase.utils.pytest_marks import *

settings = Settings()


@Priority.LOW
@decorator_loader(error_logger)
class BaseTest(unittest.TestCase):
    driver = None
    device = None
    url = None
    disable_driver = False

    def __init__(self, driver, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        super().__init__(driver)
        self.logger = self.init_logger()
        self.settings = Settings()

    @property
    def test_name(self):
        return self._testMethodName

    def init_logger(self):
        logger = logging.getLogger(self.test_name)
        logger.setLevel(logging.INFO)
        return logger

    def quit_driver(self):
        """
        Quit driver

        """
        if self.driver is not None:
            self.driver.quit()
