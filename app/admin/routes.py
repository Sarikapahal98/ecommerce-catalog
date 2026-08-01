from flask import render_template, request, redirect, url_for, flash, session, g
from app.admin import admin_bp
from app.admin.decorators import admin_required
from app.models import Product, Category, User
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
        flash('Product updated successfully!')
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

@admin_bp.route('/categories')
@admin_required
def admin_categories():
    all_categories = Category.query.all()
    return render_template('admin/categories/admin_categories.html', categories=all_categories)

@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@admin_required
def admin_add_category():
    if request.method == 'POST':
        new_category = Category(name=request.form['name'])
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully!')
        return redirect(url_for('admin.admin_categories'))
    return render_template('admin/categories/admin_add_category.html')

@admin_bp.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_category(category_id):
    category = Category.query.get_or_404(category_id)

    if request.method == 'POST':
        category.name = request.form['name']
        db.session.commit()
        flash('Category updated successfully!')
        return redirect(url_for('admin.admin_categories'))
    return render_template('admin/categories/admin_edit_category.html', category=category)

@admin_bp.route('/categories/delete/<int:category_id>')
@admin_required
def admin_delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    if category.products:
        flash(f'Cannot delete "{category.name}"- it still has products assigned to it. Reassign or delete those products first.')
        return redirect(url_for('admin.admin_categories'))

    db.session.delete(category)
    db.session.commit()
    flash('Category deleted.')
    return redirect(url_for('admin.admin_categories'))

@admin_bp.route('/users')
@admin_required
def admin_users():
    all_users = User.query.all()
    return render_template('admin/users/admin_users.html', users=all_users)

@admin_bp.route('/users/toggle-admin/<int:user_id>')
@admin_required 
def admin_toggle_admin(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == g.user.id :
        flash('An admin cannot remove thier own admin status')
        return redirect(url_for('admin.admin_users'))

    user.is_admin = not user.is_admin

    db.session.commit()
    flash('Admin status changed!')
    return redirect(url_for('admin.admin_users'))





