from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)#Creates web-application object...tells where i am running from...which folder?
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'#tells alchemy which db(store.db) to connect and how(sqlite)
db = SQLAlchemy(app)#every model class (User, Category, Product) you write will inherit from db.Model, and every query will go through this db object.                                                        


from flask import render_template
from models import Category, Product
from flask import request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask import g 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    filtered_products = Product.query.filter_by(category_id=category_id).all()
    return render_template('products.html', products=filtered_products, category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/categories')
def categories():
    all_categories = Category.query.all()
    return render_template('categories.html', categories=all_categories)

app.secret_key = 'dev-secret-key-change-later'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose another.')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email,  password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash(f'Welcome back, {user.username}!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = User.query.get(user_id) if user_id else None

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/admin')
def admin_dashboard():
    if not g.user or not g.user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('login'))
    return render_template('admin_base.html')

@app.route('/admin/products')
def admin_products():
    if not g.user or not g.user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('login'))
    all_products = Product.query.all()
    return render_template('admin_products.html', products=all_products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def admin_add_product():
    if not g.user or not g.user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('login'))
    
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
        return redirect(url_for('admin_products'))
    
    all_categories = Category.query.all()
    return render_template('admin_add_product.html', categories=all_categories)
