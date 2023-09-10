import json
from bson.objectid import ObjectId

from mongoengine import Document

import connection.connect as connect
from models.models import Authors, Quotes

def populate_authors(authors: list[dict]) -> None:
    """
    Populates the authors table
    :param authors: list of authors json objects
    :return: dictionary that contains the autor`s fullname and object mapping
    """
    authors_dict = dict()
    for obj in authors:
        author = Authors(**obj)
        author.save()



def populate_quoutes(quotes: list[dict], authors_mapping: dict[str, ObjectId]) -> None:
    """
    Populates the quotes table
    :param quotes: list of quotes json objects
    :return: None
    """
    for obj in quotes:
        author_id = authors_mapping.get(obj["author"], None)
        obj['author'] = author_id
        quote = Quotes(**obj)
        quote.save()




def main():
    with open('data/authors.json', 'r') as authors, \
        open('data/quotes.json', 'r') as quotes:
        authors_list = json.load(authors)
        quotes_list = json.load(quotes)
        print(quotes_list)

    populate_authors(authors_list)

    authors_dict = dict()
    authors_objects = Authors.objects().all()
    for obj in authors_objects:
        authors_dict.update({obj.fullname: obj.id})

    populate_quoutes(quotes_list, authors_dict)




if __name__ == '__main__':
    main()