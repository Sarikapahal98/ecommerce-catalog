from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)#Creates web-application object...tells where i am running from...which folder?
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'#tells alchemy which db(store.db) to connect and how(sqlite)
db = SQLAlchemy(app)#every model class (User, Category, Product) you write will inherit from db.Model, and every query will go through this db object.                                                        


from flask import render_template
from models import Category, Product

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