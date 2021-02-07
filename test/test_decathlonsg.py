import unittest
from test.decathlonsg_setup import Setup


class DecathlonsgHappyPath(unittest.TestCase, Setup):
    """Test case is:
      1. Go to given website
      2. Click login page button
      3. Try to logged in
      4. Go to random category page
      5. Select one random product
      6. Select product size
      7. Add product to cart
      8. Go to cart page
      9. Go to checkout page
      10. Delete items from cart and tear down
      """

    def setUp(self):
        Setup.__init__(self)

    def test_decathlonsg(self):
        self.decathlonsg_main.navigate_to_home_page()
        self.decathlonsg_main.navigate_to_login_page()
        self.decathlonsg_login.login()
        self.decathlonsg_main.navigate_to_random_category_page()
        self.decathlonsg_category.selects_random_product()
        while not self.decathlonsg_product.check_stock_info():
            self.decathlonsg_main.navigate_to_random_category_page()
            self.decathlonsg_category.selects_random_product()
        self.decathlonsg_product.add_product_to_cart()
        self.decathlonsg_main.navigate_to_cart_page()
        self.decathlonsg_cart.navigate_to_checkout_page()
        self.decathlonsg_cart.delete_items_from_cart()

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
