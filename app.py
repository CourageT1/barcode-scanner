#!/usr/bin/python3
"""Flask app for the project"""
import os
from flask import Flask, render_template, request, jsonify
from models import db, Product, FileStorage  # Import db from models
from flask_migrate import Migrate
import sys

# Create a Flask app instance
app = Flask(__name__, static_url_path='/static', template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FILE_STORAGE'] = FileStorage()

# Initialize SQLAlchemy extension with the Flask app
db.init_app(app)

# Initialize Flask-Migrate extension
migrate = Migrate(app, db)

# Create tables in the database (if they don't exist)
with app.app_context():
    db.create_all()

# Define routes

@app.route('/')
def index():
    # Render your landing page
    return render_template('landing.html')

@app.route('/scan', methods=['POST'])
def scan():
    barcode = request.form['barcode']

    # Query the database to find the product with the given barcode
    product = Product.query.filter_by(barcode=barcode).first()

    # Prepare the response data
    response = {
        'found': True if product else False,
        'product_info': {
            'name': product.name,
            'price': product.price,
            'expiry_date': product.expiry_date,
            # Add more fields as needed
        } if product else {}
    }

    # Return the response as JSON
    return jsonify(response)

@app.route('/submit_product', methods=['POST'])
def submit_product():
    # Get form data
    barcode = request.form['barcode']
    name = request.form['name']
    price = request.form['price']
    expiry_date = request.form['expiry_date']

    # Handle file upload
    file = request.files['image']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = None

    # Save the data to the database
    new_product = Product(
        barcode=barcode,
        name=name,
        price=price,
        expiry_date=expiry_date,
        image_filename=filename
    )

    db.session.add(new_product)
    db.session.commit()

    return 'Product submitted successfully!'

# Add more routes as needed

if __name__ == '__main__':
    app.run(debug=True)
