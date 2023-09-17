'''
Виберіть бібліотеку BeautifulSoup або фреймворк Scrapy. Ви повинні виконати скрапінг сайту http://quotes.toscrape.com. 
Ваша мета отримати два файли: quotes.json, куди помістіть всю інформацію про цитати з усіх сторінок сайту та authors.
json, де буде знаходитись інформація про авторів зазначених цитат. Структура файлів json повинна повністю збігатися з 
попереднього домашнього завдання. Виконайте раніше написані скрипти для завантаження json файлів у хмарну базу даних для 
отриманих файлів. Попередня домашня робота повинна коректно працювати з новою отриманою базою даних.

Додаткове завдання.
Використовуйте для скрапінгу фреймворк Scrapy. Запуск краулера повинен бути виконаний у вигляді єдиного скрипта main.py.
'''

from typing import Any

import requests
from bs4 import BeautifulSoup



class Spider():
    def __init__(self, url: str) -> None:
        self._url = None
        self.url = url
    
    @property
    def url(self) -> str:
        return self._url
    
    @url.setter
    def url(self, new_url: str) -> None:
        response = requests.get(new_url)
        if response.status_code == 200:
            self._url = new_url
        else:
            raise ValueError(f'Cannot get url - response status code {response.status_code}.')

    def parse(self, *args, **kwargs) -> Any:
        raise NotImplementedError
    

class AuthorsSpider(Spider):
    def _get_author_urls(self) -> list[str]:
        '''
        Parse author urls from the 'https://quotes.toscrape.com'
        :return: list of author urls
        '''
        urls = []
        html = requests.get(self.url)
        soup= BeautifulSoup(html.text, 'lxml')
        links = soup.select("div[class=quote] span a")
        prefix = '/author'
        for link in links:
            if link['href'].startswith(prefix):
                urls.append(self.url + link['href'])
        return urls

    def parse(self) -> list[dict[str, str]]:
        '''
        Parse authors info from the 'https://quotes.toscrape.com'
        :return: list of author info dictionaries suitable for uploading to db
        '''
        urls = self._get_author_urls()
        result = []
        authors_fullnames = []
        for url in urls:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'lxml')
            fullname = soup.select("div[class=author-details] h3[class=author-title]")[0].text
            # check whether author fullname is already in the result and skip it
            if fullname.strip() in authors_fullnames:
                continue
            # add author fullname to the list of already processed authors
            authors_fullnames.append(fullname.strip())
            born_date = soup.select("div[class=author-details] span[class=author-born-date]")[0].text
            born_location = soup.select("div[class=author-details] span[class=author-born-location]")[0].text
            description = soup.select("div[class=author-description]")[0].text
            author_info = {
                "fullname": fullname.strip(),
                "born_date": born_date.strip(),
                "born_location": born_location.strip(),
                "description": description.strip()
            }
            result.append(author_info)
        return result


class QuotesSpider(Spider):
    def parse(self) -> list[dict[str, str]]:
        '''
        Parse quotes info from the 'https://quotes.toscrape.com'
        :return: list of quote info dictionaries suitable for uploading to db
        '''
        html = requests.get(self.url)
        soup = BeautifulSoup(html.text, 'lxml')

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

