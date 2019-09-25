from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()

def getLinks(page_url):
    global pages
    html = urlopen('http://en.wikipedia.org{}'.format(page_url))
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('z tą stroną jest coś nie tak')

    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if link.attrs['href'] not in pages:
            new_pages = link.attrs['href']
            print('-'*20)
            print(new_pages)
            pages.add(new_pages)
            getLinks(new_pages)

getLinks('')