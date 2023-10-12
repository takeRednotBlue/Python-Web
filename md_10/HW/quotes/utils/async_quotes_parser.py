import requests
import aiohttp
import asyncio

from bs4 import BeautifulSoup
from concurrent import futures

BASE_URL = 'https://quotes.toscrape.com'


class Spider:
    def parse(self, *args, **kwargs):
        raise NotImplementedError


class AuthorsSpider(Spider):
    author_urls_list = []

    def __init__(self, session=None):
        self.session = session

    def _get_author_urls(self, html):
        urls = []
        soup = BeautifulSoup(html, 'lxml')
        links = soup.select("div[class=quote] span a")
        prefix = '/author'
        for link in links:
            if link['href'].startswith(prefix):
                author_url = BASE_URL + link['href']
                if author_url not in self.author_urls_list:
                    self.author_urls_list.append(author_url)
                    urls.append(author_url)
        return urls

    def _get_author_info(self, html):
        soup = BeautifulSoup(html, 'lxml')
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
    async def aparse_author_info(self, url_list):
        result = []
        for url in url_list:
            async with self.session.get(url) as response:
                html = await response.text()
                author_info = self._get_author_info(html)
                print(author_info)
                result.append(author_info)

        print(result)
        return result

    async def parse(self, response):
        urls = self._get_author_urls(response)
        result = []
        for url in urls:
            async with self.session.get(url) as response:
                html = await response.text()
                author_info = self._get_author_info(html)
                # print(author_info)
                result.append(author_info)
        return result


class QuotesSpider(Spider):
    def parse(self, html):
        soup = BeautifulSoup(html, 'lxml')

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
    def _has_next_page(html):
        soup = BeautifulSoup(html, 'lxml')
        next_page_tag = soup.select('li[class="next"]')
        if not next_page_tag:
            return False
        return True

    async def aparse(self, url: str):
        page = 1
        authors = []
        quotes = []
        async with aiohttp.ClientSession() as session:
            while True:
                if page == 1:
                    page_url = url
                else:
                    page_url = url + f'/page/{page}/'
                async with session.get(page_url) as response:
                    if response.status >= 400:
                        print('Error while fetching page, status: {}'.format(response.status))
                        continue

                    html = await response.text()
                    try:
                        self.authors_spider.session = session
                        authors_result = await self.authors_spider.parse(html)
                        quotes_result = self.quotes_spider.parse(html)
                        quotes += quotes_result
                        authors += authors_result
                        print(f'Parsed page {page}\n Number of qoutes: {len(quotes_result)}\n Number of authors: {len(authors_result)}')
                    except Exception as err:
                        print(err, f'on page {page}')
                        page += 1
                        continue

                    if not self._has_next_page(html):
                        break
                    page += 1
        print(f"Number of authors - '{len(authors)}, Number of quotes - '{len(quotes)}")
        return quotes, authors

    def _parse_page(self, page_url):
        response = requests.get(page_url)

        if response.status_code != 200:
            print('Error while fetching page, status: {}'.format(response.status_code))

        try:
            quotes_result = self.quotes_spider.parse(response)
            authors_result = self.authors_spider.parse(response)
            print(f"Parsed '{page_url}'\n Number of quotes: {len(quotes_result)}\n\
Number of authors: {len(authors_result)}")
        except Exception as err:
            print(err, f'on url {page_url}')
            return None, None

        return quotes_result, authors_result


    async def aparse_test(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(privat_ccy_api_by_date('01.12.2022')) as response:
                print('Status: ', response.status)
                print('Content-type: ', response.headers['content-type'])
                print('Cookies: ', response.cookies)
                print(response.ok)
                result = await response.json()
                exchange = list(filter(lambda x: x['currency'] in ['USD', 'EUR'], result['exchangeRate']))
                return exchange


if __name__ == '__main__':
    import datetime
    parser = QuotesParser()
    start_time = datetime.datetime.now()
    asyncio.run(parser.aparse(BASE_URL))
    end_time = datetime.datetime.now() - start_time
    print(f'Finished in {end_time.seconds} seconds.')

