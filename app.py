from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)#Creates web-application object...tells where i am running from...which folder?
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'#tells alchemy which db(store.db) to connect and how(sqlite)
db = SQLAlchemy(app)#every model class (User, Category, Product) you write will inherit from db.Model, and every query will go through this db object.                                                        