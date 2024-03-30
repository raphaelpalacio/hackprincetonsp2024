from django.db import models
from core.opmodel import opmodel
# Create your models here.


# song model as example for using the opmodel.py
class Song(opmodel):
    title = models.CharField(max_length=100) # optimize title
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    likes = models.IntegerField()

    def __str__(self):
        return self.title


