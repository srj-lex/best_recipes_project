#!/bin/bash
cd foodgram
python3 manage.py migrate
python3 manage.py load_ingredients
python3 manage.py load_tags
python3 manage.py collectstatic
gunicorn --bind 0.0.0.0:8000 foodgram.wsgi