from django.test import TestCase

from .models import Song, WithJSON_LD, WithMetaTags, WithSEOContent

# Create your tests here.

# test creating a song model that uses the WithJSON_LD and WithMetaTags abstract models and WithSEoContent


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
