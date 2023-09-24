from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=100, unique=True)
    description = models.CharField()
    born_date = models.DateTimeField(default=None)  # %B %d, %Y - March 14, 1879
    born_location = models.CharField(max_length=150)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)


class Quote(models.Model):
    quote = models.CharField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
