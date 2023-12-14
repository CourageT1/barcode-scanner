#!/usr/bin/python3
"""gunicorn configuration"""
workers = 4  # the number of workers as needed
bind = '0.0.0.0:8000'
module = 'app:app'
