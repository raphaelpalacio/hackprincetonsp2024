from .gemini import generate_content #original way
import google.generativeai as genai
from django.core import serializers
import json
import os

#two ways to use gemini generate json_ld ,original way and using Vertex AI SDK 
# https://stackoverflow.com/questions/77727695/google-gemini-api-error-defaultcredentialserror-your-default-credentials-were

def generate_json_ld(instance):  # this function time cost 5s, return a dictionary instance
    serialized_instance = instance_to_json(instance)
    prompt = "Generate a json ld using a schema from schema.org that is most appropriate for this json data: " + serialized_instance + "Your respones should only be the json_ld as as tring and nothing else, which is start with { end with }."
    json_ld_str=generate_content(prompt)
    json_ld_dict = json.loads(json_ld_str)
    return json_ld_dict


def generate_meta_tags(instance):
    serilized_instance = instance_to_json(instance)
    prompt = f" Generate a dictionary  with keys  and values could consist the Basic HTML Meta Tags. Based on the data model: {serilized_instance}. The value of description  must has about 150 words.  Your response should only be a dictionary start with only one '{' , end with only one  '}' , without any comments, without null value, both keys and values using double quote. the dictionary should contains more than 20 pairs of Key and value, do not include any og tags which are the key value start with og.  "
    meta_tags_str=generate_content(prompt)
    meta_tags_dict = json.loads(meta_tags_str)
    return meta_tags_dict

# convert django model instance to json
def instance_to_json(instance):
    return serializers.serialize("json", [instance])#return a string of json data

def generate_open_graph(instance):
    serialized_instance = instance_to_json(instance)
    prompt =f"Generate a dictionary,  with keys are name and value are the content that are appropriate for a Facebook card which also know OpenGraph html block , using the serialized data: {serialized_instance} Your response should only be a dictionary start with only one '{' , end with only one  '}' , based on ogp.me, the dictionary do not include any comments,and None value.  both keys and values using double quote.    And og:title, og:type og:image og:url are 4 required properties for every page . and You response as much as possible, but dont impute any value except the 4 properties above which are not in the serialized data."
    open_graph_str=generate_content(prompt)
    open_graph_dict = json.loads(open_graph_str)
    print(open_graph_dict)
    return open_graph_dict


def generate_twitter_card(instance):
    # make the instance.json_ld which is dictionary to a string
    serialized_instance = instance_to_json(instance)
    prompt =f"Generate a dictionary,  with keys are the names and values are the content that are appropriate for a twitter card html block , using the serialized data: {serialized_instance} Your response should only be a dictionary starts with only one '{' , end with only one  '}' , without any comments, without null value, both keys and values using double quote.     "
    twitter_card_str=generate_content(prompt)
    witter_card_dict = json.loads(twitter_card_str)
    return witter_card_dict
