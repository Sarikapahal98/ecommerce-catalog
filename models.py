from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Category {self.name}"
# print(some_category) — instead of an ugly <Category object at 0x7f...>, you'll see <Category Electronics>. Purely for your own debugging sanity.


class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.Text, nullable = True )
    image_url = db.Column(db.String(300), nullable = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))#category-Table name(lowercase converted by default) and id is its column

    category = db.relationship('Category', backref='products')#relation between product and category ...if a is category and b is product then i can write a.products=list of products of category a 2)b.category=gives you id + name of the category the product belongs to 

    def __repe__(self):
        return f"<Product {self.name}>"
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.name}>"
