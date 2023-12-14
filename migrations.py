#!/usr/bin/python3
"""handling migrations"""
from flask_migrate import Migrate
from app import app, db

migrate = Migrate(app, db)

