import os

import google.generativeai as genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel('gemini-1.0-pro')
image_model = genai.GenerativeModel('gemini-pro-vision')

config = genai.types.GenerationConfig(candidate_count=1, temperature=0.5)


def generate_content(prompt, img=None):
    if not img:
        response = text_model.generate_content(
            prompt, generation_config=config)

    else:
        response = image_model.generate_content(
            [prompt, img], generation_config=config)

    return response.text
