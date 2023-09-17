from connection.connect import connect
from cli_interface import cli_app
from models.models import Authors, Quotes
from spiders import AuthorsSpider, QuotesSpider


base_url = 'https://quotes.toscrape.com'

authors_spider = AuthorsSpider(base_url)
quotes_spider = QuotesSpider(base_url)


def main() -> None:
    authors_obj = authors_spider.parse()
    quotes_obj = quotes_spider.parse()
    Authors.save_to_db(authors_obj)

    # mapps author's fullname to its id in order to be able to make refence 
    # to authors object in database
    authors_name_to_id = dict()
    authors_objects = Authors.objects().all()
    for obj in authors_objects:
        authors_name_to_id.update({obj.fullname: obj.id})

    Quotes.save_to_db(quotes_obj, authors_name_to_id)

if __name__ == '__main__':
    main()
    cli_app()
