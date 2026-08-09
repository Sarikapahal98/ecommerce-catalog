from flask import render_template, request
from app.main import main_bp
from app.models import Category, Product

@main_bp.route('/')
def home():
    return render_template('main/index.html')

@main_bp.route('/products')
def products():
    search_query = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    page = request.args.get('page', 1, type=int)

    query = Product.query.filter_by(is_active=True)

    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))

    if category_id:
        query = query.filter_by(category_id=category_id)

    pagination = query.paginate(page=page, per_page=2, error_out=False)

    all_categories = Category.query.all()
    return render_template('main/products.html',
                            products=pagination.items,
                            pagination=pagination,
                            categories=all_categories,
                            search_query=search_query,
                            selected_category=category_id
                           )


@main_bp.route('/category/<int:category_id>')
def category_products(category_id):
    query = Product.query.filter_by(is_active=True)
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
