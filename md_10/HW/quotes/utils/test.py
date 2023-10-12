import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"


async def fetch_quote(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape_page(session, page_url, quotes, authors):
    page_html = await fetch_quote(session, page_url)
    soup = BeautifulSoup(page_html, 'html.parser')

    for quote in soup.find_all('div', class_='quote'):
        quote_text = quote.find('span', class_='text').text
        author_name = quote.find('small', class_='author').text
        quote_tags = quote.select('div[class=tags] a')
        tags: list[str] = []
        for tag in quote_tags:
            tags.append(tag.text.strip())
        author_url = BASE_URL + quote.find('a')['href']

        quotes.append({
            'quote': quote_text.strip('\u201c').strip('\u201d'),
            'author': author_name,
            'tags': tags
        })
        authors.add(author_url)


async def scrape_author(session, author_url, author_info):
    author_html = await fetch_quote(session, author_url)
    soup = BeautifulSoup(author_html, 'html.parser')

    author_name = soup.find('h3', class_='author-title').text
    author_born_date = soup.find('span', class_='author-born-date').text
    author_description = soup.find('div', class_='author-description').text.strip()
    author_born_location = soup.find('span', class_='author-born-location').text.strip()
    if author_name.strip() == 'Alexandre Dumas-fils':
        author_name = 'Alexandre Dumas fils'
    author_info.append({
        'fullname': author_name,
        'born_date': author_born_date,
        'born_location': author_born_location,
        'description': author_description,
    })


async def scrape_quotes_with_pagination():
    quotes = []
    authors = set()
    author_info = []

    async with aiohttp.ClientSession() as session:
        page_num = 1
        while True:
            page_url = f"{BASE_URL}/page/{page_num}/"
            page_html = await fetch_quote(session, page_url)
            soup = BeautifulSoup(page_html, 'html.parser')

            if "No quotes found!" in soup.text:
                break

            await scrape_page(session, page_url, quotes, authors)
            page_num += 1

        scrape_tasks = []
        for author_url in authors:
            scrape_tasks.append(scrape_author(session, author_url, author_info))

        await asyncio.gather(*scrape_tasks)

    with open('quotes.json', 'w') as quotes_file:
        json.dump(quotes, quotes_file, indent=4)

    with open('authors.json', 'w') as authors_file:
        json.dump(author_info, authors_file, indent=4)


if __name__ == "__main__":
    import datetime
    start_time = datetime.datetime.now()
    asyncio.run(scrape_quotes_with_pagination())
    end_time = datetime.datetime.now() - start_time
    print(f'Finished in {end_time.seconds} seconds.')

