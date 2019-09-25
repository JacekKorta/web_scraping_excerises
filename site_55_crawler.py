
from bs4 import BeautifulSoup
import requests


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def printContent(self):
        print('Title: {}'.format(self.title))
        print('URL: {}\n'.format(self.url))
        print(self.body)


class Website:
    def __init__(self, name, url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.title_tag = title_tag
        self.body_tag = body_tag


class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, page_obj, selector):
        selected_elems = page_obj.select(selector)
        if selected_elems is not None and len(selected_elems) > 0:
            return '\n'.join([elem.get_text() for elem in selected_elems])
        return ''

    def parse(self, site, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.title_tag)
            body = self.safeGet(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.printContent()


crawler = Crawler()

site_data = [
    ['O\'Reilly Media', 'http://oreilly.com', 'h1', 'section#product-description'],
    ['Reuters', 'http://reuters.com', 'h1', 'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu', 'h1', 'div.post-body'],
    ['New York Times', 'http://nytimes.com', 'h1', 'div.StoryBodyCompanionColumn div p']]

websites = []

for row in site_data:
    websites.append((Website(row[0], row[1], row[2], row[3])))

crawler.parse(websites[0],
              'http://shop.oreilly.com/product/0636920028154.do')
crawler.parse(websites[1],
              'http://www.reuters.com/article/us-usa-epa-pruitt-idUSKBN19W2D0')
crawler.parse(websites[2],
              'https://www.brookings.edu/blog/techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/')
crawler.parse(websites[3],
              'https://www.nytimes.com/2018/01/28/business/energy-environment/oil-boom.html')