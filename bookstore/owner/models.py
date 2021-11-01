from django.db import models


class Book(models.Model):
    book_name = models.CharField(max_length=60,unique=True)
    author = models.CharField(max_length=60)
    price = models.IntegerField()
    copies = models.IntegerField()

    def __str__(self):
        return self.book_name