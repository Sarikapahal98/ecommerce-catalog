from app import app, db
from models import Category, Product

with app.app_context():

    electronics = Category(name='Electronics')
    clothing = Category(name='Clothing')

    db.session.add_all([electronics, clothing])
    db.session.commit()

    products = [
    Product(name='Wireless Mouse', price=19.99, description='Ergonomic wireless mouse', image_url='https://placehold.co/300x300?text=Mouse', category_id=electronics.id),
    Product(name='Bluetooth Headphones', price=49.99, description='Noise-cancelling headphones', image_url='https://placehold.co/300x300?text=Headphones', category_id=electronics.id),
    Product(name='USB-C Charger', price=15.50, description='Fast charging cable', image_url='https://placehold.co/300x300?text=Charger', category_id=electronics.id),
    Product(name='Cotton T-Shirt', price=12.00, description='100% cotton, unisex', image_url='https://placehold.co/300x300?text=T-Shirt', category_id=clothing.id),
    Product(name='Denim Jacket', price=39.99, description='Classic blue denim', image_url='https://placehold.co/300x300?text=Jacket', category_id=clothing.id),
    ]

    db.session.add_all(products)
    db.session.commit()

    print("Database seeded successfully!")