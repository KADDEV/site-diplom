from flask import Blueprint, render_template, request
from app.models import Product

views = Blueprint('views', __name__)

@views.route('/')
def index():
    featured_products = Product.query.order_by(Product.created_at.desc()).limit(4).all()
    return render_template('index.html', featured_products=featured_products)

@views.route('/catalog')
def catalog():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return render_template('catalog.html', products=products)

@views.route('/about')
def about():
    return render_template('about.html')