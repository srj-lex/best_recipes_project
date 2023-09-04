#!/bin/bash
cd foodgram
gunicorn --bind 0.0.0.0:8000 foodgram.wsgi