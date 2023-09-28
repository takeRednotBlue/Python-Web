from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import AuthorForm, QuoteForm
from .models import Quote, Author, Tag
from utils import scrape_quotes_to_db  # noqa


# Create your views here.
def main(request):
    tags_with_count = Tag.objects.annotate(usage_count=Count('quote')) # noqa
    top_10_tags = sorted(tags_with_count, key=lambda x: x.usage_count, reverse=True)[:10]
    quotes = Quote.objects.all() # noqa
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get('page')
    if not page_number:
        page_obj = paginator.get_page(number='1')
    else:
        page_obj = paginator.get_page(page_number)
    return render(request, 'quotesapp/quotes.html', {'page_obj': page_obj, 'top_tags': top_10_tags})


def tag(request, tag_name):
    tags_with_count = Tag.objects.annotate(usage_count=Count('quote')) # noqa
    top_10_tags = sorted(tags_with_count, key=lambda x: x.usage_count, reverse=True)[:10]
    quotes = Quote.objects.filter(tags__name=tag_name) # noqa
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get('page')
    if not page_number:
        page_obj = paginator.get_page(number='1')
    else:
        page_obj = paginator.get_page(page_number)
    return render(request, 'quotesapp/quotes.html', {'page_obj': page_obj, 'tag': tag_name, 'top_tags': top_10_tags})


def author_info(request, author_name):
    author = Author.objects.filter(fullname=author_name)[0] # noqa
    return render(request, 'quotesapp/author.html', {'author': author})


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


@login_required
def add_quote(request):
    tags = Tag.objects.all() # noqa
    authors = Author.objects.all() # noqa

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            author = Author.objects.filter(fullname=request.POST.get('author'))[0]
            new_quote.author = author
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/quote_form.html', {"tags": tags, "authors": authors, "form": form})

    return render(request, 'quotesapp/quote_form.html', {"tags": tags, "authors": authors, "form": QuoteForm()})


def scrape_quotes(request):
    scrape_quotes_to_db()
    return redirect(to='quotesapp:main')





