from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())


def getInternalLinks(bs, include_url):
    include_url = '{}://{}'.format(urlparse(include_url).scheme, urlparse(include_url).netloc)
    internal_links = []
    for link in bs.find_all('a', href=re.compile('^(/|.*'+include_url+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                if link.attrs['href'].starswith('/'):
                    internal_links.append(include_url+link.attrs['href'])
                else:
                    internal_links.append(link.attrs['href'])

    return internal_links


def getExternalLinks(bs, exclude_url):
    external_link = []
    for link in bs.find_all('a', href=re.compile('^(http|wwww)((?!'+exclude_url+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_link:
                external_link.append(link.attrs['href'])
    return external_link


def getRandomExternalLink(starting_page):
    html = urlopen(starting_page)
    bs = BeautifulSoup(html, 'html.parser')
    external_links = getExternalLinks(bs, urlparse(starting_page).netloc)
    print(external_links)
    if len(external_links) == 0:
        print('no external links on, looking for around the site for one')
        domain = '{}://{}'.format(urlparse(starting_page).scheme, urlparse(starting_page).netloc)
        internal_links = getInternalLinks(bs, domain)
        return getRandomExternalLink(internal_links[random.randint(0,len(internal_links)-1)])
    else:
        return external_links[random.randint(0, len(external_links)-1)]


def followExternalLinksOnly(starting_site):
    external_link = getRandomExternalLink(starting_site)
    print('Random external link is: {}'.format(external_link))
    followExternalLinksOnly(external_link)


followExternalLinksOnly('http://oreilly.com')
