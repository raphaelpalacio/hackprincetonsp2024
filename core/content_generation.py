"""
This module provides functions for generating various types of content, such as JSON-LD, meta tags, OpenGraph dictionaries,
Twitter card dictionaries, and SEO content based on instance data.

Functions:
- instance_to_json(instance): Converts a Django model instance to JSON format.
- generate_json_ld(instance): Generate a JSON-LD using a schema from schema.org that is most appropriate for the given JSON data.
- generate_meta_tags(instance): Generate a dictionary with keys and values that could consist of the Basic HTML Meta Tags.
- generate_open_graph(instance): Generate an OpenGraph dictionary for a Facebook card based on the provided instance.
- generate_twitter_card(instance): Generate a dictionary with keys as the names and values as the content that are appropriate for a Twitter card HTML block.
- generate_seo_content(instance): Generate SEO content based on the instance data.
"""

import json
import os

import google.generativeai as genai
from django.core import serializers

from .gemini import generate_content


def instance_to_json(instance):
    """
    Converts a Django model instance to JSON format.

    Args:
        instance: The Django model instance to be converted.

    Returns:
        A JSON string representing the serialized instance.
    """
    return serializers.serialize("json", [instance])


def generate_json_ld(instance):
    """
    Generate a JSON-LD using a schema from schema.org that is most appropriate for the given JSON data.

    Args:
        instance: The JSON data to be converted to JSON-LD.

    Returns:
        dict: The generated JSON-LD as a dictionary.

    Raises:
        ValueError: If the generated content is not a valid JSON-LD.
    """
    serialized_instance = instance_to_json(instance)
    prompt = "Generate a JSON-LD using a schema from schema.org that is most appropriate for this JSON data: " + \
        serialized_instance + \
        "Your response should only be the JSON-LD as a string and nothing else, which should start with '{' and end with '}'."

    json_ld_str = generate_content(prompt)
    json_ld_dict = json.loads(json_ld_str)
    return json_ld_dict


def generate_meta_tags(instance):
    """
    Generate a dictionary with keys and values that could consist of the Basic HTML Meta Tags.

    Args:
        instance: The instance object used to generate the meta tags.

    Returns:
        A dictionary containing the generated meta tags.
    """
    serialized_instance = instance_to_json(instance)
    prompt = f" Generate a dictionary with keys and values that could consist the Basic HTML Meta Tags. Based on the data model: {serialized_instance}. The value of description must have about 150 words. Your response should only be a dictionary starting with only one '{' , ending with only one '}', without any comments, without null values, and both keys and values using double quotes. The dictionary should contain more than 20 pairs of key-value, but should not include any og tags (key-value pairs starting with 'og')."
    meta_tags_str = generate_content(prompt)
    meta_tags_dict = json.loads(meta_tags_str)
    return meta_tags_dict


def generate_open_graph(instance):
    """
    Generate an OpenGraph dictionary for a Facebook card based on the provided instance.

    Args:
        instance: The instance to generate the OpenGraph dictionary for.

    Returns:
        The generated OpenGraph dictionary.

    Raises:
        None.
    """
    serialized_instance = instance_to_json(instance)
    prompt = f"Generate a dictionary,  with keys are name and value are the content that are appropriate for a Facebook card which also know OpenGraph html block , using the serialized data: {serialized_instance} Your response should only be a dictionary start with only one '{' , end with only one  '}' , based on ogp.me, the dictionary do not include any comments,and None value.  both keys and values using double quote.    And og:title, og:type og:image og:url are 4 required properties for every page . and You response as much as possible, but dont impute any value except the 4 properties above which are not in the serialized data."
    open_graph_str = generate_content(prompt)
    open_graph_dict = json.loads(open_graph_str)
    return open_graph_dict


def generate_twitter_card(instance):
    """
    Generate a dictionary with keys as the names and values as the content that are appropriate for a Twitter card HTML block.

    Args:
        instance: The instance to be serialized and used for generating the Twitter card dictionary.

    Returns:
        A dictionary containing the appropriate content for a Twitter card HTML block.
    """
    serialized_instance = instance_to_json(instance)
    prompt = f"Generate a dictionary, with keys as the names and values as the content that are appropriate for a Twitter card HTML block, using the serialized data: {serialized_instance}. Your response should only be a dictionary starting with only one '{' and ending with only one '}', without any comments, without null values, and both keys and values using double quotes."
    twitter_card_str = generate_content(prompt)
    twitter_card_dict = json.loads(twitter_card_str)
    return twitter_card_dict


def generate_seo_content(instance):
    """
    Generate SEO content based on the instance data.

    Args:
        instance: An instance containing data for generating SEO content.

    Returns:
        str: The generated SEO content in a valid HTML format.
    """
    prompt = """Generate SEO content based off of the instance data.
        The content must include one H1 tag that contains the most relevant keywords in the instance data.
        The content generated must contain at least one H2 tag.
        The content must include at least 500 total words of content separated in as many paragraph tags as necessary and divided into whatever heading structure necessary.
        The LLM output should be in a valid HTML format using heading tags and paragraph tags only.
        Here is the instance data: """

    if hasattr(instance, 'json_ld') and instance.json_ld is not None:
        prompt += str(getattr(instance.json_ld, 'data', ''))
    if hasattr(instance, 'meta_tags') and instance.meta_tags is not None:
        prompt += str(getattr(instance.meta_tags, 'data', ''))
    if hasattr(instance, 'open_graph') and instance.open_graph is not None:
        prompt += str(getattr(instance.open_graph, 'data', ''))
    if hasattr(instance, 'twitter_card') and instance.twitter_card is not None:
        prompt += str(getattr(instance.twitter_card, 'data', ''))

    data = generate_content(prompt)

    return data
