from Project import Scraper
import unittest

class Test_Scraper(unittest.TestCase):
    def setUp(self) -> None:
        self.product = Scraper()
        return super().setUp()

    def test_store_one_data(self):
        product_list=["Title","Price","Status","Image","SKU","Link","UUID","Product_Type"]
        expect_value = 8
        product_dict = self.product.store_one_data(product_list)
        actual_value = len(product_dict)
        self.assertEqual(actual_value,expect_value)
        self.assertNotEqual(actual_value,7)
        self.assertIsInstance(product_dict,dict)

    def test_get_all_product_links(self):
        self.product.driver.get("https://store.eu.square-enix-games.com/en_GB")
        actual_value = self.product.get_all_product_links()
        self.assertIsInstance(actual_value, list)

    def tearDown(self) -> None:
        del self.product
        return super().tearDown()
    pass
unittest.main(argv=[''], verbosity=0 ,exit=False)