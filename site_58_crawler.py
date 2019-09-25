from bs4 import BeautifulSoup
import requests


class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.url = url
        self.body = body

    def printContent(self):
        print('New article found for topic: {}'.format(self.topic))
        print('URL: {}'.format(self.url))
        print('Title: {}'.format(self.title))
        print('Body:n{}'.format(self.body))


class Website:
    def __init__(self, name, url, search_url, result_listing, result_url, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.search_url = search_url
        self.result_listing = result_listing
        self.result_url = result_url
        self.absolute_url = absolute_url
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
        child_obj = page_obj.select(selector)
        if child_obj is not None and len(child_obj) > 0:
            return child_obj[0].get_text()
        return ''

    def search(self, topic, site):
        bs = self.getPage(site.search_url + topic)
        search_results = bs.select(site.result_listing)
        for result in search_results:
            url = result.select(site.result_url)[0].attrs['href']
            if site.absolute_url:
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print('Something was wrong with that page or URL. Skipping!')
                return
            title = self.safeGet(bs, site.title_tag)
            body = self.safeGet(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(topic, title, body, url)
                content.printContent()


crawler = Crawler()

siteData = [
    ['O\'Reilly Media', 'http://oreilly.com', 'https://ssearch.oreilly.com/?q=',
     'article.product-result', 'p.title a', True, 'h1','section#product-description'],
    ['Reuters', 'http://reuters.com', 'http://www.reuters.com/search/news?blob=',
     'div.search-result-content', 'h3.search-result-title a', False, 'h1','div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu','https://www.brookings.edu/search/?s=',
     'div.list-content article','h4.title a', True, 'h1', 'div.post-body']
    ]

sites = []

for row in siteData:
    sites.append(Website(row[0], row[1], row[2],row[3], row[4], row[5], row[6], row[7]))

topics = ['python', 'data science']
for topic in topics:
    print('GETTING INFO ABOUT: ' + topic)
    for target_site in sites:
        crawler.search(topic, target_site)