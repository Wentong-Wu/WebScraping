import unittest
from Scraper import Scraper

class Test_Scraper(unittest.TestCase):

    def test_accept_cookies(self):
        assert Scraper.accept_cookies(self)
        #self.assertEqual(sum([1,1]), 3, "Should be 6")
        pass

    def test_get_product(self):

        pass

    def test_get_age_restriction(self):

        pass

    def test_get_one_data(self):

        pass

    def test_get_all_data(self):

        pass

    pass

if __name__ == "__main__":
    unittest.main()