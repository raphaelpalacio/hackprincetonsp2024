import json

import PIL.Image
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from ..gemini import generate_content


def instance_to_json(instance):
    data = serializers.serialize('json', [instance])
    return data


def get_related_object(instance):
    """
    Returns the related object associated with the current instance.

    Returns:
        object: The related object.
    """

    for related_object in instance._meta.related_objects:
        if related_object.one_to_one:
            try:
                related_object = getattr(
                    instance, related_object.get_accessor_name())
                return related_object

            except ObjectDoesNotExist:
                continue
    return None


class JsonLD(models.Model):
    """
    Represents a JSON_LD object.

    Attributes:
        data (JSONField): The JSON data associated with the object.
    """

    DEFAULT_PROMPT = "Generate a JSON-LD using a schema from schema.org that is most appropriate for the JSON data provided below. Your response should only be the JSON-LD as a string and nothing else, which should start with the opening curly braces character '{' and end with closing curly braces character '}'."

    data = models.JSONField(null=True)
    prompt = models.TextField(default=DEFAULT_PROMPT)

    def generate(self):
        """
        Generate a JSON-LD using a schema from schema.org that is most appropriate for the given JSON data.

        Args:
            instance: The JSON data to be converted to JSON-LD.

        Returns:
            dict: The generated JSON-LD as a dictionary.

        Raises:
            ValueError: If the generated content is not a valid JSON-LD.
        """

        related_object = get_related_object(self)
        json_string = instance_to_json(related_object)
        json_ld = generate_content(self.prompt + json_string)
        print("my json_ld", json_ld)
        dictionary = json.loads(json_ld)
        self.data = dictionary
        self.save()

    def to_html(self):
        """
        Returns the JSON-LD data as a script tag.

        Returns:
            str: The JSON-LD data wrapped in a script tag.
        """

        return f'<script type="application/ld+json">{json.dumps(self.data)}</script>'


class MetaTags(models.Model):
    """
    Represents the metadata tags associated with a specific model instance.
    """

    DEFAULT_PROMPT = "Generate a dictionary with keys and values that could consist the Basic HTML Meta Tags. Based on the data model below. The value of description must have about 150 words. Your response should only be a dictionary starting with only one '{' , ending with only one '}', without any comments, without null values, and both keys and values using double quotes. The dictionary should contain more than 20 pairs of key-value, but should not include any og tags (key-value pairs starting with 'og')."

    data = models.JSONField(null=True)
    prompt = models.TextField(default=DEFAULT_PROMPT)

    def generate(self):
        """
        Generate a dictionary with keys and values that could consist of the Basic HTML Meta Tags.

        Args:
            instance: The instance object used to generate the meta tags.

        Returns:
            A dictionary containing the generated meta tags.
        """

        related_object = get_related_object(self)
        json_string = instance_to_json(related_object)
        meta_tags = generate_content(self.prompt + json_string)
        dictionary = json.loads(meta_tags)
        self.data = dictionary
        self.save()

    def to_html(self):
        """
        Generates the HTML meta tags based on the data stored in the `meta_tags` field.

        Returns:
            str: The HTML meta tags as a string.
        """

        output = ""
        for key, value in self.data.items():
            output += f'<meta name="{key}" content="{value}">\n'

        return output


class OpenGraph(models.Model):
    """
    Represents the metadata tags associated with a specific model instance.
    """

    DEFAULT_PROMPT = "Generate a dictionary, with keys are name and value are the content that are appropriate for a Facebook card which also know OpenGraph html block , using the serialized data below. Your response should only be a dictionary start with only one '{' , end with only one  '}' , based on ogp.me, the dictionary do not include any comments,and None value.  both keys and values using double quote.    And og:title, og:type og:image og:url are 4 required properties for every page . and You response as much as possible, but dont impute any value except the 4 properties above which are not in the serialized data."

    data = models.JSONField(null=True)
    prompt = models.TextField(default=DEFAULT_PROMPT)

    def generate(self):
        """
        Generate an OpenGraph dictionary for a Facebook card based on the provided instance.

        Args:
            instance: The instance to generate the OpenGraph dictionary for.

        Returns:
            The generated OpenGraph dictionary.

        Raises:
            None.
        """

        related_object = get_related_object(self)
        json_string = instance_to_json(related_object)
        open_graph_tags = generate_content(self.prompt + json_string)
        dictionary = json.loads(open_graph_tags)
        self.data = dictionary
        self.save()

    def to_html(self):
        """
        Retrieves the Open Graph data as HTML meta tags.

        Returns:
            str: The Open Graph data as HTML meta tags.
        """

        output = ""
        for key, value in self.open_graph.data.items():
            output += f'<meta property="og:{key}" content="{value}">\n'

        return output


class TwitterCard(models.Model):
    """
    Represents a Twitter card.

    Attributes:
        data (JSONField): A field containing the data for the Twitter card.
        prompt (TextField): A field containing the prompt for generating the Twitter card.
    """

    DEFAULT_PROMPT = "Generate a dictionary, with keys as the names and values as the content that are appropriate for a Twitter card HTML block, using the serialized data below. Your response should only be a dictionary starting with only one '{' and ending with only one '}', without any comments, without null values, and both keys and values using double quotes."

    data = models.JSONField(null=True)
    prompt = models.TextField(default=DEFAULT_PROMPT)

    def generate(self):
        """
        Generate a Twitter card dictionary based on the provided instance.

        Args:
            instance: The instance to generate the Twitter card dictionary for.

        Returns:
            The generated Twitter card dictionary.

        Raises:
            None.
        """

        related_object = get_related_object(self)
        json_string = instance_to_json(related_object)
        twitter_card_str = generate_content(self.prompt + json_string)
        dictionary = json.loads(twitter_card_str)
        self.data = dictionary
        self.save()

    def to_html(self):
        """
        Retrieves the Twitter card data as HTML meta tags.

        Returns:
            str: The Twitter card data as HTML meta tags.
        """

        output = ""
        for key, value in self.data.items():
            output += f'<meta name="twitter:{key}" content="{value}">\n'

        return output


class SEOContent(models.Model):
    """
    Represents SEO content for a webpage.

    Attributes:
        data (JSONField): A field containing the data for the SEO content.
        prompt (TextField): A field containing the prompt for generating the SEO content.
    """

    DEFAULT_PROMPT = """Generate SEO content based off of the instance data.
            The content must include one H1 tag that contains the most relevant keywords in the instance data.
            The content generated must contain at least one H2 tag.
            The content must include at least 500 total words of content separated in as many paragraph tags as necessary and divided into whatever heading structure necessary.
            The LLM output should be in a valid HTML format using heading tags and paragraph tags only.
            Here is the instance data: """

    data = models.TextField(null=True)
    prompt = models.TextField(default=DEFAULT_PROMPT)

    def generate(self):
        """
        Generate a SEO content dictionary based on the provided instance.

        Args:
            instance: The instance to generate the SEO content dictionary for.

        Returns:
            The generated SEO content dictionary.

        Raises:
            None.
        """

        related_object = get_related_object(self)
        prompt = self.prompt

        if hasattr(related_object, 'json_ld') and related_object.json_ld is not None:
            prompt += str(getattr(related_object.json_ld, 'data', ''))
        if hasattr(related_object, 'meta_tags') and related_object.meta_tags is not None:
            prompt += str(getattr(related_object.meta_tags, 'data', ''))
        if hasattr(related_object, 'open_graph') and related_object.open_graph is not None:
            prompt += str(getattr(related_object.open_graph, 'data', ''))
        if hasattr(related_object, 'twitter_card') and related_object.twitter_card is not None:
            prompt += str(getattr(related_object.twitter_card, 'data', ''))

        content = generate_content(prompt)

        self.data = content
        self.save()

    def to_html(self):
        """
        Retrieves the SEO content data as HTML meta tags.

        Returns:
            str: The SEO content data as HTML meta tags.
        """

        return self.data


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

    DEFAULT_ALT_PROMPT = "Analyze the contents of this image and generate 125 character that are search engine optimized for the alt attribute in the HTML img tag for this image. It is very important that your response is under 125 characters. Do your best to generate the most search engine optimized response and descriptive. Your response should be only the alt text to be used and nothing else: "
    DEFAULT_JSON_LD_PROMPT = "Generate a json-ld valid string starting with the opening curly braces character '{' and ending with the closing curly braces character '}' following a schema.org schema for the main object in the image. Have { as the first character of your response and } and the last character of your response. Your json-ld should contain all the fields you can fill out in the chosen schema. Your response should be solely valid json ld string. Your response must start with the opening curly braces character '{' and end with closing curly braces character '}'. You are not allowed to have any other character in the beginning or end of your response."

    image = models.ImageField(upload_to='images/')

    alt = models.CharField(max_length=125, null=True, blank=True)
    alt_prompt = models.TextField(default=DEFAULT_ALT_PROMPT)

    json_ld = models.JSONField(null=True, blank=True)
    json_ld_prompt = models.TextField(default=DEFAULT_JSON_LD_PROMPT)

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

        super().save(*args, **kwargs)  # Save first to get an ID

        if not self.alt and not self.json_ld:
            self.generate()

    def generate(self):
        """
        Generate the alternative text for the image.

        Returns:
            str: The generated alternative text.
        """

        img = PIL.Image.open(self.image.path)

        print("my old alt", self.alt)
        self.alt = generate_content(self.alt_prompt, img)
        print("my new alt", self.alt)

        json_ld_string = generate_content(self.json_ld_prompt, img)
        self.json_ld = json.loads(json_ld_string)

        super(AnalyzedImage, self).save()
