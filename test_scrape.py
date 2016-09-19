from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest
from types import *

from scrape_operations import ScrapeOperations


class TestSainsbury(unittest.TestCase):

    def setUp(self):
        self.url = "http://en.wikipedia.org/wiki/Monty_Python"
        self.bsObj = BeautifulSoup(urlopen(self.url))

    def _contentExists(self, products):
        try:
            for product in products.select('li'):

                    title_select = product.select('.productInfo h3 a')
                    self.assertNotEqual(title_select, None)
                    price_select = product.select('.pricePerUnit')
                    self.assertNotEqual(price_select, None)

                    title = title_select[0].get_text().strip()
                    assert type(title) is StringType, "title is not a string: %r" % title

                    description = ScrapeOperations.get_description(title_select[0].get('href'))
                    assert type(description) is StringType, "description is not a string: %r" % description

                    page_size = ScrapeOperations.get_page_size(title_select[0].get('href'))
                    assert type(page_size) is StringType, "pagesize is not a string: %r" % page_size

                    unit_price = ScrapeOperations.extract_price(price_select[0].get_text())
                    assert type(unit_price) is FloatType, "unitprice is not an float: %r" % id
            return True

        except AttributeError as e:
            return False

    def test_scrape_page(self):
        self.assertNotEqual(self.bsObj, None)
        self.assertNotEqual(ScrapeOperations.get_page_size(self.url), None)

        products = self.bsObj.find('ul', attrs={'class': 'productLister'})
        self.assertNotEqual(products, None)

        self.assertTrue(self._contentExists(products))

        print("Done!")

if __name__ == '__main__': unittest.main()