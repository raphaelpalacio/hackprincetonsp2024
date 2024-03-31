
from django.db import models

from core.models import (AnalyzedImage, WithJsonLD, WithMetaTags,
                         WithOpenGraph, WithSEOContent, WithTwitterCard)

# Create your models here.


class Song(WithJsonLD, WithSEOContent, WithTwitterCard, models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()


class Car(WithJsonLD, WithMetaTags, WithOpenGraph, models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.OneToOneField(AnalyzedImage, on_delete=models.CASCADE)
