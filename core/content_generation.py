import json

from django.core import serializers

from .gemini import generate_content


def instance_to_json(instance):
    # return a string of json data
    return serializers.serialize("json", [instance])

# this function time cost 5s, return a dictionary instance


def generate_json_ld(instance):
    serialized_instance = instance_to_json(instance)
    prompt = "Generate a json ld using a schema from schema.org that is most appropriate for this json data: " + \
        serialized_instance + \
        "Your respones should only be the json_ld as as tring and nothing else, which is start with { end with }."
    json_ld_str = generate_content(prompt)
    json_ld_dict = json.loads(json_ld_str)
    return json_ld_dict


def generate_meta_tags(instance):
    return {"title": "fake meta title", "description": "fake meta description"}


def generate_open_graph(instance):
    pass


def generate_twitter_card(instance):
    data = instance.json_ld.data
    return data


def generate_seo_content(instance):
    # a prompt that asks an LLM to generate SEO content based off of the instance. The prompt should use the json_ld, meta_tags, open_graph, and twitter_card attributes of the instance to prompt the LLM to generate SEO optimized content. The content must include one H1 tag that contains the most relevant keywords in the instance data. The content generated must contain at least one H2 tag. The content must include at least 500 total words of content separated in as many paragraph tags as necessary and divided into whatever heading structure necessary. The LLM output should be in a valid HTML format using heading tags and paragraph tags only.
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
