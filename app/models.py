from app import db
from app import login
from datetime import datetime, timedelta
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import base64
import os

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

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page':page,
                'per_page':per_page,
                'total_pages': resources.pages,
                'total_items':resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class User(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
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

    def add_grocery(self, grocery):
        grocery.price = int(float(grocery.price) * 100)
        self.groceries.append(grocery)
        db.session.add(grocery)
        db.session.add(self)
        db.session.commit()

    def add_meal(self, meal):
        self.meals.append(meal)
        db.session.add(meal)
        db.session.add(self)
        db.session.commit()

    def add_menu(self, menu):
        self.menus.append(menu)
        db.session.add(menu)
        db.session.add(self)
        db.session.commit()

    def add_store(self, store):
        self.stores.append(store)
        db.session.add(store)
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self, include_email=False):
        data = {
            'id':self.id,
            'username': self.username,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'groceries': '<groceries>',
                'menus': '<menus>',
                'meals': '<meals>',
                'stores': '<stores>'
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
            if new_user and 'password' in data:
                self.set_password(data['password'])

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    price = db.Column(db.Integer)
    count = db.Column(db.Integer)
    stores = db.relationship('Store',
                             secondary=grocery_meal_map)

    def add_store(self, store):
        self.stores.append(store)
        db.session.add(store)
        db.session.add(self)
        db.session.commit()

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    groceries = db.relationship('Grocery',
                                secondary=grocery_meal_map)
    menus = db.relationship('Menu',
                            secondary=grocery_meal_map)

    def add_menu(self, menu):
        self.menus.append(menu)
        db.session.add(menu)
        db.session.add(self)
        db.session.commit()

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meals = db.relationship('Meal',
                            secondary=grocery_meal_map)

    def add_meal(self, meal):
        self.meals.append(meal)
        db.session.add(meal)
        db.session.add(self)
        db.session.commit()

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    groceries = db.relationship('Grocery',
                                secondary=grocery_meal_map)

    def add_grocery(self, grocery):
        self.groceries.append(grocery)
        db.session.add(meal)
        db.session.add(self)
        db.session.commit()
