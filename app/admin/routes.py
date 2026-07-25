from flask import render_template, request, redirect, url_for, flash
from app.admin import admin_bp
from app.admin.decorators import admin_required
from app.models import Product, Category
from app import db

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    return render_template('admin/admin_base.html')

@admin_bp.route('/products')
@admin_required
def admin_products():
    all_products = Product.query.all()
    return render_template('admin/products/admin_products.html', products=all_products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    if request.method == 'POST':
        new_product = Product(
            name=request.form['name'],
            price=float(request.form['price']),
            description=request.form['description'],
            image_url=request.form['image_url'],
            category_id=int(request.form['category_id'])
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('admin.admin_products'))
    
    all_categories = Category.query.all()
    return render_template('admin/products/admin_add_product.html', categories=all_categories)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.description = request.form['description']
        product.image_url = request.form['image_url']
        product.category_id = int(request.form['category_id'])
        db.session.commit()
        flash('Product updaated successfully!')
        return redirect(url_for('admin.admin_products'))
    
    all_categories = Category.query.all()
    return render_template('admin/products/admin_edit_product.html', product=product, categories=all_categories)

@admin_bp.route('/products/delete/<int:product_id>')
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted. ')
    return redirect(url_for('admin.admin_products'))

