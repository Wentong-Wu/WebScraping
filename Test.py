import unittest
from Scraper import Scraper

class Test_Scraper(unittest.TestCase):
    
    def test_store_one_data(self):
        self.product_list=["Title","Price","Status","Image","SKU","Link","UUID","Product_Type"]
        self.expect_value = 8
        self.product_dict = Scraper.store_one_data(self,self.product_list)
        self.actual_value = len(self.product_dict)
        self.assertEqual(self.actual_value,self.expect_value)

if __name__ == "__main__":
    unittest.main(exit=False)