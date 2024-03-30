from django.test import TestCase

from core.models import Song, Author



class jsonld_test(TestCase):
    # Create your tests here.
    # write the function to testing models
    obj=Song(title="song1",artist="artist1",album="album1",genre="genre1",release_date="2021-01-01",likes=1)
    obj.save()
