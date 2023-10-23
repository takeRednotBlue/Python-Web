import os
import asyncio
# import json
from datetime import datetime
import django

from utils.quotes_parser import scrape_quotes_with_pagination, BASE_URL  # noqa
from quotesapp.models import Quote, Tag, Author  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')
django.setup()


def scrape_quotes_to_db(scraper=scrape_quotes_with_pagination):
    quotes, authors = asyncio.run(scraper())
    # with open('quotes.json', 'w') as quotes_file, open('authors.json', 'w') as authors_file:
    #     json.dump(quotes, quotes_file, indent=4)
    #     json.dump(authors, authors_file, indent=4)
    # with open('quotes.json', 'r+') as quotes_file, open('authors.json', 'r+') as authors_file:
    #     quotes = json.load(quotes_file)
    #     authors = json.load(authors_file)

    for author in authors:
        author['born_date'] = datetime.strptime(
            author['born_date'], '%B %d, %Y').date()
        Author.objects.get_or_create(**author)

    for quote in quotes:
        tags = []
        for tag in quote['tags']:
            t, *_ = Tag.objects.get_or_create(name=tag)
            tags.append(t)

        author = Author.objects.filter(fullname=quote['author']).all()[0]

        quote_exists = bool(len(Quote.objects.filter(quote=quote['quote'])))
        if not quote_exists:
            new_quote = Quote.objects.create(
                quote=quote['quote'],
                author=author,
            )
            for tag in tags:
                new_quote.tags.add(tag)
