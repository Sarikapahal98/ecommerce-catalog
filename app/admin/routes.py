from flask import render_template, request, redirect, url_for, flash, session, g
from app.admin import admin_bp
from app.admin.decorators import admin_required
from app.models import Product, Category, User, ProductImage, SiteSettings
from app import db

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    return render_template('admin/admin_base.html')

@admin_bp.route('/products')
@admin_required
def admin_products():
    search_query = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    page = request.args.get('page', 1, type=int)

    query = Product.query

    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))

    if category_id:
        query = query.filter_by(category_id=category_id)

    pagination = query.paginate(page=page, per_page=3, error_out=False)

    all_categories = Category.query.all()

    return render_template('admin/products/admin_products.html',
                            products=pagination.items,
                            pagination=pagination,
                            categories=all_categories,
                            search_query=search_query,
                            selected_category=category_id)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    if request.method == 'POST':
        new_product = Product(
            name=request.form['name'],
            price=float(request.form['price']),
            discount_percent=float(request.form.get('discount_percent', 0) or 0),
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
        product.discount_percent = float(request.form.get('discount_percent', 0) or 0)
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

@admin_bp.route('/users/toggle-admin/<int:user_id>', methods=['POST'])
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

@admin_bp.route('/products/toggle-status/<int:product_id>')
@admin_required
def admin_toggle_product_status(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_active = not product.is_active
    db.session.commit()
    flash(f'{product.name} is now {"active" if product.is_active else "disabled"}.')
    return redirect(url_for('admin.admin_products'))

@admin_bp.route('/user/toggle-status/<int:user_id>')
@admin_required
def admin_toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == g.user.id:
        flash('You cannot disable your own account.')
        return redirect(url_for('admin.admin_users'))
    user.is_active = not user.is_active
    db.session.commit()
    flash(f'{user.username} is now {"active" if user.is_active else "disabled"}.')
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/category/toggle-status/<int:category_id>')
@admin_required
def admin_toggle_category_status(category_id):
    category = Category.query.get_or_404(category_id)
    category.is_active = not category.is_active
    db.session.commit()
    flash(f'{category.name} is now {"active" if category.is_active else "disabled"}.')
    return redirect(url_for('admin.admin_categories'))
    
@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('admin.admin_users'))

    return render_template('admin/users/admin_edit_user.html', user=user)

@admin_bp.route('/products/<int:product_id>/images', methods=['GET', 'POST'])
@admin_required
def admin_product_images(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        new_image_url = request.form['image_url'].strip()
        if new_image_url:
            new_image = ProductImage(image_url=new_image_url, product_id=product.id)
            db.session.add(new_image)
            db.session.commit()
            flash('Image added!')
        return redirect(url_for('admin.admin_product_images', product_id=product.id))
    return render_template('admin/products/admin_product_images.html', product=product)

@admin_bp.route('/products/images/delete/<int:image_id>')
@admin_required
def admin_delete_product_image(image_id):
    image = ProductImage.query.get_or_404(image_id)
    product_id = image.product_id
    db.session.delete(image)
    db.session.commit()
    flash('Image removed.')
    return redirect(url_for('admin.admin_product_images', product_id=product_id))


@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    settings = SiteSettings.query.first()

    if request.method == 'POST':
        settings.site_name = request.form['site_name']
        settings.tagline = request.form['tagline']
        settings.logo_url = request.form['logo_url']
        settings.contact_email = request.form['contact_email']
        settings.contact_phone = request.form['contact_phone']
        db.session.commit()
        flash('Settings updated')
        return redirect(url_for('admin/settings/admin_settings.html', settings=settings))
    return render_template('admin/settings/admin_settings.html', settings=settings)

    
