from flask import render_template
from app.main import main_bp
from app.models import Category, Product

@main_bp.route('/')
def home():
    return render_template('main/index.html')

@main_bp.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('main/products.html', products=all_products)


@main_bp.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    filtered_products = Product.query.filter_by(category_id=category_id).all()
    return render_template('main/products.html', products=filtered_products, category=category)

@main_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('main/product_detail.html', product=product)

@main_bp.route('/categories')
def categories():
    all_categories = Category.query.all()
    return render_template('main/categories.html', categories=all_categories)
