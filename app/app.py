#!/usr/bin/python3
"""Flask app forthe project"""
import os
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
import sys
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

# Create a Flask app instance
app = Flask(__name__, static_url_path='/static', template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize SQLAlchemy extension with the Flask app
db.init_app(app)
# Initialize Flask-Migrate extension
migrate = Migrate(app, db)

# Create tables in the database (if they don't exist)
with app.app_context():
    db.create_all()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.String(20))
    promotion = db.Column(db.String(100))
    image_filename = db.Column(db.String(100))

# Define routes

@app.route('/')
def index():
    # Render your landing page
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Handle favicon.ico request
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/promotion')
def promotions():
    return render_template('promotions.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

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
