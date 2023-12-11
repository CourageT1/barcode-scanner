#!/usr/bin/python3
"""database storage"""
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
photos = UploadSet("photos", IMAGES)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.String(20))
    promotion = db.Column(db.String(100))
    image_filename = db.Column(db.String(100))
