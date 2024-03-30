import json

import PIL.Image
from django.db import models

from .content_generation import (generate_json_ld, generate_meta_tags,
                                 generate_open_graph, generate_seo_content,
                                 generate_twitter_card)
from .gemini import generate_content


class JSON_LD(models.Model):
    data = models.JSONField()


class WithJSON_LD(models.Model):
    json_ld = models.OneToOneField(
        JSON_LD, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.json_ld:
            print("my json ld created")
            data = generate_json_ld(self)
            self.json_ld = JSON_LD.objects.create(data=data)
            self.json_ld.save()

        else:
            json_ld = self.json_ld
            data = generate_json_ld(self)
            json_ld.data = data
            json_ld.save()

        super().save(*args, **kwargs)

    def get_json_ld(self):
        return f'<script type="application/ld+json">{json.dumps(self.json_ld.data)}</script>'

    class Meta:
        abstract = True


class MetaTags(models.Model):
    data = models.JSONField()


class WithMetaTags(models.Model):
    meta_tags = models.OneToOneField(
        MetaTags, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.meta_tags:
            print("my meta tag created")
            data = generate_meta_tags(self)
            self.meta_tags = MetaTags.objects.create(data=data)
            self.meta_tags.save()

        else:
            print("my not meta tag")
            meta_tags = self.meta_tags
            data = generate_meta_tags(self)
            meta_tags.data = data
            meta_tags.save()

        super().save(*args, **kwargs)

    def get_meta_tags(self):
        output = ""
        for key, value in self.meta_tags.data.items():
            output += f'<meta name="{key}" content="{value}">\n'

        return output

    class Meta:
        abstract = True


class OpenGraph(models.Model):
    data = models.JSONField()


class WithOpenGraph(models.Model):
    open_graph = models.OneToOneField(
        OpenGraph, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.open_graph:
            data = generate_open_graph(self)
            self.open_graph = OpenGraph.objects.create(data=data)
            self.open_graph.save()

        else:
            open_graph = self.open_graph
            data = generate_open_graph(self)
            open_graph.data = data
            open_graph.save()

        super().save(*args, **kwargs)

    def get_open_graph(self):
        output = ""
        for key, value in self.open_graph.data.items():
            output += f'<meta property="og:{key}" content="{value}">\n'

        return output

    class Meta:
        abstract = True


class TwitterCard(models.Model):
    data = models.JSONField()


class WithTwitterCard(models.Model):
    twitter_card = models.OneToOneField(
        TwitterCard, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.twitter_card:
            data = generate_twitter_card(self)
            self.twitter_card = TwitterCard.objects.create(data=data)
            self.twitter_card.save()

        else:
            twitter_card = self.twitter_card
            data = generate_twitter_card(self)
            twitter_card.data = data
            twitter_card.save()

        super().save(*args, **kwargs)

    def get_twitter_card(self):
        output = ""
        for key, value in self.twitter_card.data.items():
            output += f'<meta name="twitter:{key}" content="{value}">\n'

        return output

    class Meta:
        abstract = True


class SEOContent(models.Model):
    data = models.JSONField()


class WithSEOContent(models.Model):
    seo_content = models.OneToOneField(
        SEOContent, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.seo_content:
            print("my seo content created")
            data = generate_seo_content(self)
            self.seo_content = SEOContent.objects.create(data=data)
            self.seo_content.save()

        else:
            seo_content = self.seo_content
            data = generate_seo_content(self)
            seo_content.data = data
            seo_content.save()

        super().save(*args, **kwargs)

    def get_seo_content(self):
        return self.seo_content.data

    class Meta:
        abstract = True


class AnalyzedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    alt = models.CharField(max_length=125, null=True, blank=True)
    json_ld = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)

        img = PIL.Image.open(self.image.path)
        if not self.alt:
            self.alt = generate_content(
                "Analyze the contents of this image and generate 125 character that are search engine optimized for the alt attribute in the HTML img tag for this image. It is very important that your response is under 125 characters. Do your best to generate the most search engine optimized response and descriptive. Your response should be only the alt text to be used and nothing else: ", img)

        if not self.json_ld:
            content = generate_content(
                "Attempt to identify the main object of this image. After identifying the main object of the image, try to define all attributes for it given its characteristic and generate a json-ld valid string following a schema.org schema. Your json-ld should contain all the fields you can fill out in chosen schema. The schema you choose should be the one that is most appropriate for the single main object you identified in the image. Your response should be solely valid json string that can be converted to a json object directly with python function json.loads and absolutely nothing else", img)
            content = content[8:-3]
            print("my content", content)
            self.json_ld = json.loads(content)
        super().save(*args, **kwargs)


class Song(WithJSON_LD, WithMetaTags, WithSEOContent, models.Model):
    """Example model that a developer using our package may have"""

    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
