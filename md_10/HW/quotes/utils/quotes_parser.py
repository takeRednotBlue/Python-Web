import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://quotes.toscrape.com'


class Spider:
    def parse(self, *args, **kwargs):
        raise NotImplementedError


class AuthorsSpider(Spider):

    author_urls_list = []
    def _get_author_urls(self, response):
        urls = []
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.select("div[class=quote] span a")
        prefix = '/author'
        for link in links:
            if link['href'].startswith(prefix):
                author_url = BASE_URL + link['href']
                if author_url not in self.author_urls_list:
                    self.author_urls_list.append(author_url)
                    urls.append(author_url)
        return urls

    def _get_author_info(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        fullname = soup.select("div[class=author-details] h3[class=author-title]")[0].text
        born_date = soup.select("div[class=author-details] span[class=author-born-date]")[0].text
        born_location = soup.select("div[class=author-details] span[class=author-born-location]")[0].text
        description = soup.select("div[class=author-description]")[0].text
        # handles case when the author info fullname doesn't match that in quote info
        if fullname.strip() == 'Alexandre Dumas-fils':
            fullname = 'Alexandre Dumas fils'
        author_info = {
            "fullname": fullname.strip(),
            "born_date": born_date.strip(),
            "born_location": born_location.strip(),
            "description": description.strip()
        }
        return author_info

    def parse(self, response):
        urls = self._get_author_urls(response)
        result = []
        for url in urls:
            author_info = self._get_author_info(url)
            result.append(author_info)
        return result


class QuotesSpider(Spider):
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        result = []
        quote_blocks = soup.select('div[class=quote]')
        quote_selector = 'span[class=text]'
        author_selector = 'span small[class=author]'
        tags_selector = 'div[class=tags] a'
        for quote in quote_blocks:
            quote_text = quote.select(quote_selector)[0].text
            quote_author = quote.select(author_selector)[0].text
            quote_tags = quote.select(tags_selector)
            tags: list[str] = []
            for tag in quote_tags:
                tags.append(tag.text.strip())
            result.append({
                'tags': tags,
                'author': quote_author.strip(),
                'quote': quote_text.strip('\u201c').strip('\u201d'),
            })
        return result


class QuotesParser:
    def __init__(self, quotes_spider=QuotesSpider(), authors_spider=AuthorsSpider()):
        self.quotes_spider = quotes_spider
        self.authors_spider = authors_spider

    @staticmethod
    def _has_next_page(response):
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        next_page_tag = soup.select('li[class="next"]')
        if not next_page_tag:
            return False
        return True

    def parse(self, url: str):
        page = 1
        authors = []
        quotes = []
        while True:
            if page == 1:
                page_url = url
            else:
                page_url = url + f'/page/{page}/'
            response = requests.get(page_url)

            if response.status_code != 200:
                print('Error while fetching page, status: {}'.format(response.status_code))
                continue

            try:
                quotes_result = self.quotes_spider.parse(response)
                authors_result = self.authors_spider.parse(response)
                quotes += quotes_result
                authors += authors_result
                # print(f'Parsed page {page}\n Number of qoutes: {len(quotes)}\n Number of authors: {len(authors)}')
            except Exception as err:
                print(err, f'on page {page}')
                page += 1
                continue

            if not self._has_next_page(response):
                break
            page += 1

        return quotes, authors
