import requests
from bs4 import BeautifulSoup


# parser
class Scraper(object):

    def __init__(self, url):
        self.url = url
        # create a variable which will store a list of quotes
        quotes = []

        # retrieve data from the link and save it as an object
        respond = requests.get(url)

        # get a source code from the page
        soup = BeautifulSoup(respond.content, 'html.parser')

        # find all div tags with class='sodatext'
        for element in soup.find_all('div', attrs={'class': 'sodatext'}):
            # keep only text skipping tags
            quote = element.text.strip()
            # make it more comprehensive
            quote = quote.replace(':\n', ': ').replace(']\n', ']').replace(']', '] ')
            # add to the list
            quotes.append(quote)
        self.quotes = quotes
