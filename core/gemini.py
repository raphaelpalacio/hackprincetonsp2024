"""
This module is used to interact with the Gemini Generative AI models.

It uses the Gemini API to generate content based on a given prompt. 
If an image is provided, it uses the image model to generate content, 
otherwise, it uses the text model.

Environment Variables:
- GEMINI_API_KEY: The API key for the Gemini service.

Functions:
- generate_content(prompt, img=None): Generates content based on the provided prompt and optional image.
"""

import os

import google.generativeai as genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel('gemini-1.0-pro')
image_model = genai.GenerativeModel('gemini-pro-vision')

config = genai.types.GenerationConfig(candidate_count=1, temperature=0.5)


def generate_content(prompt, img=None):
    """
    Generate content based on the given prompt and optional image.

    Args:
        prompt (str): The prompt to generate content from.
        img (str, optional): The image to use as additional input for content generation. Defaults to None.

    Returns:
        str: The generated content.
    """

    if not img:
        response = text_model.generate_content(
            prompt, generation_config=config)

    else:
        response = image_model.generate_content(
            [prompt, img], generation_config=config)

    return response.text
