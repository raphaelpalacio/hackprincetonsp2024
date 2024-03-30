# Getting Started

Execute:

1. `python3 -m venv env` create a Python virtual environment
2. `source env/bin/activate` activate virtual environment
3. `pip install -r requirements.txt` install dependencies
4. `python manage.py makemigrations`
5. `python manage.py migrate`

Setting Environmental Variable(MAC):
`Export GEMINI_API_KEY="Your GEMINI KEY"`

# Project Structure

webtune/

It contains the main Django project configs and info

core/

The app we will develop. It is convention to name the main app in your project `core`.

_Discord webhook test_
