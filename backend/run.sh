#!/bin/bash
cd foodgram
python3 manage.py migrate
python3 manage.py load_ingridients
python3 manage.py collectstatic
cp -r /backend/foodgram/collected_static/. /backend_static/static/
gunicorn --bind 0.0.0.0:8000 foodgram.wsgi