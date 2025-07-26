# Webtune

A Python library that harnesses the efficiency and richness of semantic functions to optimize website SEO performance, leveraging the power of Gemini.

## Description:

Elevate your Django web application effortlessly with custom actions tailored to rejuvenate JSON-LD, meta tags, Open Graph tags, Twitter Card tags, SEO content, and analyzed images, seamlessly accessible and controllable via the intuitive Django admin interface. Guaranteeing search engine crawlers access to precise and pertinent information about your website's content semantically. This feature not only amplifies organic traffic but also empowers your site to effectively engage with search engine algorithms - amplifying its online visibility and discoverability like never before.

Execute:

1. `python3 -m venv env` create a Python virtual environment
2. `source env/bin/activate` activate virtual environment
3. `pip install -r requirements.txt` install dependencies
4. `python manage.py makemigrations`
5. `python manage.py migrate`

Setting Environmental Variable(MAC):
`Export GEMINI_API_KEY="Your GEMINI KEY"`

## Project Structure

webtune/

It contains the main Django project configs and info

core/

The app we will develop. It is convention to name the main app in your project `core`.
