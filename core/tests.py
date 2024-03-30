from django.test import TestCase
from core.models import Song
from core.content_generation import instance_to_json
from core.content_generation import generate_json_ld
from core.content_generation import generate_twitter_card
from core.content_generation import generate_open_graph
from core.content_generation import generate_meta_tags

import json

from .models import Song, WithJSON_LD, WithMetaTags, WithSEOContent

# Create your tests here.
# test creating a song model that uses the WithJSON_LD and WithMetaTags abstract models and WithSEoContent
        
# test song model and instance_to_json function
class SongTestCase(TestCase):
    def setUp(self):
        Song.objects.create(title="test song", artist="test artist", album="Test alum")

    #passed
    def test_song(self):
        song = Song.objects.get(title="test song")
        jsons=instance_to_json(song)
      #  print(jsons)
    #passed
    def test_json_ld(self):
        song = Song.objects.get(title="test song")
        json_ld=generate_json_ld(song)
        #print(json_ld) # this will print a json dictionary

    #passed
    # def test_generate_twitter_card(self):
    #     song = Song.objects.get(title="test song")
    #     twitter_card_dict=generate_twitter_card(song)
    #     print(twitter_card_dict)
    
    #passed
    # def test_generate_open_graph(self):
    #     song = Song.objects.get(title="test song")
    #     open_graph_dict=generate_open_graph(song)
    #     print(open_graph_dict)

    def test_meta_tags(self):
        song = Song.objects.get(title="test song")
        meta_tags_dict=generate_meta_tags(song)
        print(meta_tags_dict)

# Rafael testss
class SongModelTestCase(TestCase):
    def test_song_model(self):
        # Create a song instance
        song = Song.objects.create(
            title="Hello", artist="Adele", album="My First Kiss")

        # Check if the song instance has the expected attributes and methods
        # self.assertTrue(hasattr(song, 'json_ld'))
        # self.assertTrue(hasattr(song, 'meta_tags'))
        # self.assertTrue(hasattr(song, 'seo_content'))

        # Check if the song instance inherits from the abstract models
        # self.assertIsInstance(song, WithJSON_LD)
        # self.assertIsInstance(song, WithMetaTags)
        # self.assertIsInstance(song, WithSEOContent)

        # Print attributes
        print(dir(song))
        print("my ld", song.get_json_ld())
        print("my meta", song.get_meta_tags())
        print("my content", song.get_seo_content())
