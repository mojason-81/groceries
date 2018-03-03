from app import db
from app import login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

grocery_meal_map = db.Table(
    'grocery_meal_map',
    db.Column('grocery_id', db.Integer, db.ForeignKey('grocery.id')),
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id')),
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id')),
    db.Column('store_id', db.Integer, db.ForeignKey('store.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    groceries = db.relationship('Grocery',
                                secondary=grocery_meal_map,
                                backref='user', lazy='dynamic')
    meals = db.relationship('Meal',
                            secondary=grocery_meal_map,
                            backref='user', lazy='dynamic')
    menus = db.relationship('Menu',
                            secondary=grocery_meal_map,
                            backref='user', lazy='dynamic')
    stores = db.relationship('Store',
                             secondary=grocery_meal_map,
                             backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    price = db.Column(db.Integer)
    count = db.Column(db.Integer)
    stores = db.relationship('Store',
                             secondary=grocery_meal_map)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    groceries = db.relationship('Grocery',
                                secondary=grocery_meal_map)
    menus = db.relationship('Menu',
                            secondary=grocery_meal_map)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meals = db.relationship('Meal',
                            secondary=grocery_meal_map)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(60), index=True)
    groceries = db.relationship('Grocery',
                                secondary=grocery_meal_map)
