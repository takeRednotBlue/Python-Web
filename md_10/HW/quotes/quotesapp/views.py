from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AuthorForm
from .models import Quote, Author, Tag
from quotesapp.scraping.quotes_parser import QuotesParser, BASE_URL  # noqa


# Create your views here.
def main(request):
    # seed_db()
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get('page')
    if not page_number:
        page_obj = paginator.get_page(number='1')
    else:
        page_obj = paginator.get_page(page_number)
    return render(request, 'quotesapp/quotes.html', {'page_obj': page_obj})


def tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name=tag_name)
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get('page')
    if not page_number:
        page_obj = paginator.get_page(number='1')
    else:
        page_obj = paginator.get_page(page_number)
    return render(request, 'quotesapp/quotes.html', {'page_obj': page_obj, 'tag': tag_name})


def author_info(request, author_name):
    author = Author.objects.filter(fullname=author_name)[0]
    return render(request, 'quotesapp/author_form.html', {'author': author})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/author_form.html', {"form": form})

    return render(request, 'quotesapp/author_form.html', {"form": AuthorForm()})


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



