from scrape_operations import ScrapeOperations
import sys
import json


def _get_json(arg):

    html = ScrapeOperations.get_html(arg)
    if html is None:
        return 'HTML could not be found'

    return json.dumps(ScrapeOperations.get_products(html))


def main():
    args = sys.argv[1:]

    if len(args) == 0:
            sys.exit('Usage: scrape.py  "html argument"')

    else:
        print (args[0])
        print(_get_json(args[0]))


if __name__ == '__main__':
    main()
