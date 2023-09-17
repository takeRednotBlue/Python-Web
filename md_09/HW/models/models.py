from bson import ObjectId

from mongoengine import Document
from mongoengine.fields import StringField, ListField, ReferenceField


class Authors(Document):
    fullname = StringField(required=True, max_length=50, unique=True)
    born_date = StringField(required=True, max_length=20)
    born_location = StringField(required=True, max_length=100)
    description = StringField(required=True)

    @classmethod
    def save_to_db(cls, authors_objects: list[dict]) -> None:
        '''
        Save data to database
        :param authors_objects: list of dictionaries containing authors information
        '''
        for obj in authors_objects:
            author = cls(**obj)
            author.save()

class Quotes(Document):
    quote = StringField(required=True)
    tags = ListField(StringField(), required=True)
    author = ReferenceField(Authors)

    @classmethod
    def save_to_db(cls, quotes_objects: list[dict], authors_mapping: dict[str, ObjectId]) -> None:
        '''
        Save data to database
        :param quotes_objects: list of dictionaries containing quotes information
        :param authors_mapping: dictionary that maps authors fullnames to authors id
        in order to be able to make reference
        '''
        for obj in quotes_objects:
            author_id = authors_mapping.get(obj["author"], None)
            obj['author'] = author_id
            quote = cls(**obj)
            quote.save()


