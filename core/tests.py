from django.test import TestCase
from core.models import Song
from core.content_generation import instance_to_json
from core.content_generation import generate_json_ld
from core.content_generation import generate_twitter_card

import json

# Create your tests here.

# test song model and instance_to_json function
class SongTestCase(TestCase):
    def setUp(self):
        Song.objects.create(title="test song", artist="test artist", album="Test alum")

    def test_song(self):
        song = Song.objects.get(title="test song")
        jsons=instance_to_json(song)
        print(jsons)

    def test_json_ld(self):
        song = Song.objects.get(title="test song")
        json_ld=generate_json_ld(song)
        print(json_ld) # this will print a json dictionary

    def test_generate_twitter_card(self):
        song = Song.objects.get(title="test song")
        twitter_card=generate_twitter_card(song)
        print(type(twitter_card))