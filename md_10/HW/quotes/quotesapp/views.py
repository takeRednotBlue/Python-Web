from datetime import datetime
import json

from django.shortcuts import render

from .models import Quote, Author, Tag
from quotesapp.scraping.quotes_parser import QuotesParser, BASE_URL


# Create your views here.
def main(request):
    # seed_db()
    quotes = Quote.objects.all()
    return render(request, 'quotesapp/quotes.html', {'quotes': quotes})


def tag(request):
    pass


def seed_db():
    # parser = QuotesParser()
    # quotes, authors = parser.start_parse(BASE_URL)
    # with open('quotes.json', 'w') as quotes_file, open('authors.json', 'w') as authors_file:
    #     json.dump(quotes, quotes_file, indent=4)
    #     json.dump(authors, authors_file, indent=4)
    with open('quotes.json', 'r+') as quotes_file, open('authors.json', 'r+') as authors_file:
        quotes = json.load(quotes_file)
        authors = json.load(authors_file)
    for author in authors:
        print(author['fullname'])
        author['born_date'] = datetime.strptime(author['born_date'], '%B %d, %Y')
        author = Author(**author)
        author.save()

    tags_set = set()
    for quote in quotes:
        for item in quote['tags']:
            tags_set.add(item)

    for item in tags_set:
        tag = Tag(name=item)
        tag.save()

    for quote in quotes:
        text = quote['quote']
        # print(repr(quote['author']))
        author = Author.objects.filter(fullname=quote['author']).all()[0]
        new_quote = Quote(
            quote=text,
            author=author,
        )
        new_quote.save()
        choice_tags = Tag.objects.filter(name__in=quote['tags'])
        for tag in choice_tags.iterator():
            new_quote.tags.add(tag)


if __name__ == '__main__':
    seed_db()



