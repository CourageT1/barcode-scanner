#!/usr/bin/python3
""" Gunicorn configuration file"""
workers = 4
module_name = "app"
app_name = "app"

bind = "0.0.0.0:8000"
