import unittest
from Scraper import Scraper

class Test_Scraper(unittest.TestCase):

    def test_get_all_product_by_catogary(self):
        list_catogary = ["games","merchandise"]
        assert Scraper.get_all_product_by_catogary(list_catogary) 
        pass

    pass

if __name__ == "__main__":
    unittest.main()