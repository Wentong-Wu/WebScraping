import unittest
from unittest.mock import Mock
from Scraper import Scraper

class Test_Scraper(unittest.TestCase):
    
    def setUp(self) -> None:
        self.product = Scraper()
        return super().setUp()

    def test_store_one_data(self):
        self.product_list=["Title","Price","Status","Image","SKU","Link","UUID","Product_Type"]
        self.expect_value = 8
        self.product_dict = self.product.store_one_data(self.product_list)
        self.actual_value = len(self.product_dict)
        self.assertEqual(self.actual_value,self.expect_value)
        self.assertNotEqual(self.actual_value,7)
        self.assertIsInstance(self.product_dict,dict)

    def test_get_all_product_links(self):
        self.product.driver.get("https://store.eu.square-enix-games.com/en_GB")
        actual_value = self.product.get_all_product_links()
        self.assertIsInstance(actual_value, list)

    def tearDown(self) -> None:
        del self.product
        return super().tearDown()
if __name__ == "__main__":
    unittest.main(exit=True)