#!/usr/bin/python3
"""Flask app for the project"""
import os
from flask import Flask, render_template, request, jsonify
from models import db, Product, FileStorage
import barcode
from barcode.writer import ImageWriter

# Create a Flask app instance
app = Flask(__name__, static_url_path='/static', template_folder='templates')

# Configurations for Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FILE_STORAGE'] = FileStorage()

# Initialize SQLAlchemy extension with the Flask app
db.init_app(app)

# Create tables in the database (if they don't exist)
with app.app_context():
    db.create_all()

# Define routes

# Route for the home page
@app.route('/')
def index():
    """Render the home page."""
    products = Product.query.all()
    return render_template('index.html', products=products)

# Route for the landing page
@app.route('/landing')
def landing():
    return render_template('landing.html')

# Route for the "About" page
@app.route('/about')
def about():
    about_content = """
    Shopping Made Easy is your go-to solution for a hassle-free shopping experience. 
    Our barcode scanner app simplifies the process of finding and purchasing your favorite items.
    Scan barcodes, explore promotions, and enjoy the convenience of efficient shopping. Shopping made easy.
    """
    return render_template('about.html', about_content=about_content)

# Route for the "Promotions" page
@app.route('/promotions')
def promotions():
    # For simplicity, promotions are hardcoded here. In a real app, you would fetch these from a database.
    promotions_list = ['promotion1.jpg', 'promotion2.jpg']
    return render_template('promotions.html', promotions_list=promotions_list)

# Route for the "Scan" page
@app.route('/scan')
def scan():
    return render_template('scan.html')

# Route for the "Contact" page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Run the Flask app if this script is executed
if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
