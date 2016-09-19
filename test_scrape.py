from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest


from scrape_operations import ScrapeOperations


class TestSainsbury(unittest.TestCase):

    def setUp(self):
        self.url = "http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html"
        self.bsObj = BeautifulSoup(urlopen(self.url))

    def _contentExists(self, products):
        try:
            for product in products.select('li'):
                title_select = product.select('.productInfo h3 a')
                self.assertNotEqual(title_select, None)
                price_select = product.select('.pricePerUnit')
                self.assertNotEqual(price_select, None)

                title = title_select[0].get_text().strip()
                print (title)
                self.assertTrue(isinstance(title, str))

                description = ScrapeOperations.get_description(title_select[0].get('href'))
                self.assertTrue(isinstance(description, str))

                page_size = ScrapeOperations.get_page_size(title_select[0].get('href'))
                self.assertTrue(isinstance(page_size, str))

                unit_price = ScrapeOperations.extract_price(price_select[0].get_text())
                self.assertTrue(isinstance(float(unit_price), float))

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