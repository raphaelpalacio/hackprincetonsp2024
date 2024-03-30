import json

from django.db import models

from .content_generation import (generate_json_ld, generate_meta_tags,
                                 generate_open_graph, generate_twitter_card)


class JSON_LD(models.Model):
    data = models.JSONField()


class WithJSON_LD(models.Model):
    json_ld = models.OneToOneField(
        JSON_LD, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.json_ld:
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
        if not self.id:
            data = generate_meta_tags(self)
            self.meta_tags = MetaTags.objects.create(data=data)
            self.meta_tags.save()

        else:
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
        if not self.id:
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


class Song(WithJSON_LD, WithTwitterCard, models.Model):
    """Example model that a developer using our package may have"""

    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
