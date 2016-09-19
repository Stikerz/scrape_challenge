from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import re


class ScrapeOperations(object):

    @staticmethod
    def get_html(url):
        try:
            html = urlopen(url)
            return html
        except HTTPError as e:
            return None

    @staticmethod
    def get_page_size(url):
        try:
            h = requests.head(url)
            content_length = h.headers.get('Content-Length')
            size = int(content_length)
            size = round(size / 1024, 1)
            return '%skb' % size
        except HTTPError as e:
            return None

    @staticmethod
    def extract_price(price_string):

        price = re.findall(r"[-+]?\d*\.\d+|\d+", price_string)

        if len(price) == 1:
            return price.pop()
        else:
            return None

    @staticmethod
    def get_description(url):

        html = ScrapeOperations.get_html(url)
        if html:
            try:
                bss_obj = BeautifulSoup(html.read())
                description = bss_obj.select('htmlcontent .productText')[0].get_text().strip()
                return description
            except AttributeError as e:
                return None
        else:
            return None

    @staticmethod
    def total_unit_prices(products):

        total = sum([float(product['unit_price']) for product in products])
        total = format(total, '.2f')

        return total

    @staticmethod
    def get_products(html):

        try:
            bss_obj = BeautifulSoup(html.read())
            products = bss_obj.find('ul', attrs={'class': 'productLister'})

            if products is None:
                raise AttributeError('Class productLister not found')
            product_list = []
            for product in products.select('li'):

                title_select = product.select('.productInfo h3 a')
                price_select = product.select('.pricePerUnit')

                if title_select and price_select:
                    title = title_select[0].get_text().strip()
                    description = ScrapeOperations.get_description(title_select[0].get('href'))
                    page_size = ScrapeOperations.get_page_size(title_select[0].get('href'))
                    unit_price = ScrapeOperations.extract_price(price_select[0].get_text())

                    product_list.append({'title': title,
                                         'unit_price': unit_price,
                                         'size': page_size,
                                         'description': description
                                         })

            return {
                'results': product_list,
                'total': ScrapeOperations.total_unit_prices(product_list)
            }

        except AttributeError as e:
            return None
