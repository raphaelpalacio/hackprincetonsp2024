"""
This module contains the models used in the application for handling various types of content generation and management.

The models in this file include:
- JSON_LD: A model for storing JSON-LD data.
- WithJSON_LD: An abstract model that provides functionality for generating and managing JSON-LD data.
- MetaTags: A model for storing meta tags data.
- WithMetaTags: An abstract model that provides functionality for generating and managing meta tags data.
- OpenGraph: A model for storing Open Graph data.
- WithOpenGraph: An abstract model that provides functionality for generating and managing Open Graph data.
- TwitterCard: A model for storing Twitter Card data.
- WithTwitterCard: An abstract model that provides functionality for generating and managing Twitter Card data.
- SEOContent: A model for storing SEO content data.
- WithSEOContent: An abstract model that provides functionality for generating and managing SEO content data.
- AnalyzedImage: A model for storing analyzed image data, including alt text and JSON-LD.

Each abstract model provides a `save` method that generates the corresponding content data if it does not exist, and updates the data if it already exists. The generated content is based on the attributes of the model instance.

The `AnalyzedImage` model also overrides the `save` method to generate alt text and JSON-LD data for the uploaded image.

Note: This file assumes the existence of other modules such as `content_generation` and `gemini` for the actual content generation logic.
"""

import json

import PIL.Image
from django.db import models

from .content_generation import (generate_json_ld, generate_meta_tags,
                                 generate_open_graph, generate_seo_content,
                                 generate_twitter_card)
from .gemini import generate_content


class JSON_LD(models.Model):
    """
    Represents a JSON_LD object.

    Attributes:
        data (JSONField): The JSON data associated with the object.
    """

    data = models.JSONField()


class WithJSON_LD(models.Model):
    """
    A base abstract model that provides functionality for generating and saving JSON-LD data.

    Attributes:
        json_ld (OneToOneField): A one-to-one relationship field to the JSON_LD model.
    """

    json_ld = models.OneToOneField(
        JSON_LD, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate and save JSON-LD data.

        If the json_ld attribute is not set, it generates JSON-LD data using the generate_json_ld function
        and creates a new JSON_LD object with the generated data. Otherwise, it updates the existing JSON_LD
        object with the new data.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

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
        """
        Returns the JSON-LD data as a script tag.

        Returns:
            str: The JSON-LD data wrapped in a script tag.
        """

        return f'<script type="application/ld+json">{json.dumps(self.json_ld.data)}</script>'

    class Meta:
        abstract = True


class MetaTags(models.Model):
    """
    Represents the metadata tags associated with a specific model instance.
    """

    data = models.JSONField()


class WithMetaTags(models.Model):
    """
    A base abstract model that provides functionality for managing meta tags.

    This class should be inherited by other models that require meta tags.
    """

    meta_tags = models.OneToOneField(
        MetaTags, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to handle the creation and updating of meta tags.

        If the `meta_tags` field is not set, it creates a new `MetaTags` object
        and associates it with the current instance. Otherwise, it updates the
        existing `MetaTags` object with new data.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """

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
        """
        Generates the HTML meta tags based on the data stored in the `meta_tags` field.

        Returns:
            str: The HTML meta tags as a string.
        """

        output = ""
        for key, value in self.meta_tags.data.items():
            output += f'<meta name="{key}" content="{value}">\n'

        return output

    class Meta:
        abstract = True


class OpenGraph(models.Model):
    """
    Represents an Open Graph object.

    Attributes:
        data (dict): The Open Graph data associated with the object.
    """

    data = models.JSONField()


class WithOpenGraph(models.Model):
    """
    A base model class that provides functionality for generating and retrieving Open Graph data.

    This class should be used as a base class for models that require Open Graph integration.

    Attributes:
        open_graph (OneToOneField): A one-to-one relationship field to the OpenGraph model.

    Methods:
        save(*args, **kwargs): Overrides the save method to generate and save Open Graph data.
        get_open_graph(): Retrieves the Open Graph data as HTML meta tags.

    Meta:
        abstract = True
    """

    open_graph = models.OneToOneField(
        OpenGraph, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate and save Open Graph data.

        If the model instance does not have an associated Open Graph object, it generates the data
        using the generate_open_graph function and creates a new OpenGraph object with the data.
        If the model instance already has an associated Open Graph object, it updates the data in
        the existing object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
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
        """
        Retrieves the Open Graph data as HTML meta tags.

        Returns:
            str: The Open Graph data as HTML meta tags.
        """

        output = ""
        for key, value in self.open_graph.data.items():
            output += f'<meta property="og:{key}" content="{value}">\n'

        return output

    class Meta:
        abstract = True


class TwitterCard(models.Model):
    """
    Represents a Twitter card.

    Attributes:
        data (dict): A dictionary containing the data for the Twitter card.
    """

    data = models.JSONField()


class WithTwitterCard(models.Model):
    """
    A mixin class that provides functionality for generating and managing Twitter cards.

    Attributes:
        twitter_card (TwitterCard): A one-to-one relationship field to the TwitterCard model.

    Methods:
        save(*args, **kwargs): Overrides the save method to generate and save a Twitter card if it doesn't exist, or update an existing one.
        get_twitter_card(): Returns the HTML meta tags for the Twitter card data.
    """

    twitter_card = models.OneToOneField(
        TwitterCard, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate and save a Twitter card if it doesn't exist, or update an existing one.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

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
        """
        Returns the HTML meta tags for the Twitter card data.

        Returns:
            str: The HTML meta tags for the Twitter card data.
        """

        output = ""
        for key, value in self.twitter_card.data.items():
            output += f'<meta name="twitter:{key}" content="{value}">\n'

        return output

    class Meta:
        abstract = True


class SEOContent(models.Model):
    """
    Represents SEO content for a webpage.

    Attributes:
        data (dict): A JSONField that stores the SEO content data.
    """

    data = models.JSONField()


class WithSEOContent(models.Model):
    """
    A base model class that provides SEO content functionality.

    This class is intended to be inherited by other models that require SEO content.
    It provides methods for generating and retrieving SEO content.

    Attributes:
        seo_content (SEOContent): The SEO content associated with the model.

    Methods:
        save(*args, **kwargs): Overrides the default save method to handle SEO content creation and updates.
        get_seo_content(): Retrieves the SEO content data associated with the model.
    """

    seo_content = models.OneToOneField(
        SEOContent, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to handle SEO content creation and updates.

        If the model does not have an associated SEO content, it generates the content
        using the generate_seo_content function and creates a new SEOContent object.
        If the model already has an associated SEO content, it updates the content.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

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
        """
        Retrieves the SEO content data associated with the model.

        Returns:
            The SEO content data.
        """

        return self.seo_content.data

    class Meta:
        abstract = True


class AnalyzedImage(models.Model):
    """
    Represents an analyzed image with additional attributes.

    Attributes:
        image (ImageField): The uploaded image.
        alt (CharField): The alternative text for the image.
        json_ld (JSONField): The JSON-LD representation of the image.

    Methods:
        save(*args, **kwargs): Overrides the default save method to perform additional operations.
    """

    image = models.ImageField(upload_to='images/')
    alt = models.CharField(max_length=125, null=True, blank=True)
    json_ld = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to perform additional operations.

        If the object is being saved for the first time, it generates the alternative text (alt) for the image
        by analyzing its contents. It also generates the JSON-LD representation of the image if it doesn't exist.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """

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
