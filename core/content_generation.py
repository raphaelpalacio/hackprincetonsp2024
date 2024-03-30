from .gemini import generate_content #original way
import google.generativeai as genai
from django.core import serializers
import json
import os

#two ways to use gemini generate json_ld ,original way and using Vertex AI SDK 
# https://stackoverflow.com/questions/77727695/google-gemini-api-error-defaultcredentialserror-your-default-credentials-were

def generate_json_ld(instance):  # this function time cost 5s, return a dictionary instance
    GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro')

    serialized_instance = instance_to_json(instance)
    prompt = "Generate a json ld using a schema from schema.org that is most appropriate for this json data: " + serialized_instance + "Your respones should only be the json_ld as as tring and nothing else, which is start with { end with }."
    json_ld_str=generate_content(prompt)
    json_ld_dict = json.loads(json_ld_str)
    return json_ld_dict


def generate_meta_tags(instance):
    pass

# convert django model instance to json
def instance_to_json(instance):
    return serializers.serialize("json", [instance])#return a string of json data

def generate_open_graph(instance):
    pass


def generate_twitter_card(instance):
    # make the instance.json_ld which is dictionary to a string
    data=str(instance.json_ld)
    return data
