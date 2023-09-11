from mongoengine import Document
from mongoengine.fields import StringField, ListField, ReferenceField

class Authors(Document):
    fullname = StringField(required=True, max_length=50)
    born_date = StringField(required=True, max_length=20)
    born_location = StringField(required=True, max_length=100)
    description = StringField(required=True)


class Quotes(Document):
    quote = StringField(required=True)
    tags = ListField(StringField(), required=True)
    author = ReferenceField(Authors)


