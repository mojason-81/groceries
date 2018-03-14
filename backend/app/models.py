from app import db
from app import login
from datetime import datetime, date, timedelta
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import base64
import os

grocery_meal_map = db.Table(
    'grocery_meal_map',
    db.Column('grocery_id', db.Integer, db.ForeignKey('grocery.id')),
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'))
)

meal_menu_map = db.Table(
    'meal_menu_map',
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id')),
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'))
)

# grocery_store_map...  perhaps this association table could hold the price of the grocery item.
# This could be an association object with the extra data on this table.
# See: http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# The class passed in must inherit from db.Model.
def inspect_table(cls):
    return {
        'columns': dict(cls.__table__.columns),
        'foreign_keys': cls.__table__.foreign_keys,
        'constraints': cls.__table__.foreign_keys
    }

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, user_id, page, per_page, endpoint, **kwargs):
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
                'self': url_for(endpoint, id=user_id, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, id=user_id, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, id=user_id, page=page - 1, per_page=per_page,
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
                                backref='user', lazy='dynamic')
    meals = db.relationship('Meal',
                            backref='user', lazy='dynamic')
    menus = db.relationship('Menu',
                            backref='user', lazy='dynamic')
    stores = db.relationship('Store',
                             backref='user', lazy='dynamic')

    def add_groceries(self, groceries):
        for grocery in groceries:
            grocery.price = int(float(grocery.price) * 100)
            self.groceries.append(grocery)
            db.session.add(grocery)
            db.session.add(self)
        db.session.commit()

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

    def add_stores(self, stores):
        for store in stores:
            self.stores.append(store)
            db.session.add(store)
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

    def to_dict(self, include_email=False, include_token=False):
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
        if include_token:
            # FIXME: this token isn't yet committed.
            data['token'] = self.get_token()
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
            if new_user and 'password' in data:
                self.set_password(data['password'])

    def __repr__(self):
        # TODO: maybe return a jsonify'd dictionary?
        # return str({ 'id': self.id, 'username': self.username, 'email': self.email})
        return "<User: {},\n username: {},\n email: {}>".format(self.id, self.username, self.email)

class Grocery(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    name = db.Column(db.String(60), index=True)
    price = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def add_to_store(self, store):
        self.stores.append(store)
        db.session.add(store)
        db.session.add(self)
        db.session.commit()

    def add_to_meal(self, meal):
        meal.groceries.append(self)
        db.session.add(meal)
        db.session.commit()

    def to_dict(self,):
        data = {
            'id':self.id,
            'name': self.name,
            'price': self.price / 100,
            'count': self.count,
            '_links': {
                'self': url_for('api.get_grocery', user_id=self.user.id, id=self.id),
                'user': url_for('api.get_user', id=self.user.id),
                'menus': '<menus>',
                'meals': '<meals>',
                'stores': '<stores>'
            }
        }
        return data

    def __repr__(self):
        # TODO: maybe return a jsonify'd dictionary?
        return "<Grocery: {},\n name: {},\n price: {},\n count: {},\n stores: {}>".format(self.id,
                                                                                         self.name,
                                                                                         (self.price / 100),
                                                                                         self.count,
                                                                                         '<stores>')

class Meal(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'))
    name = db.Column(db.String(60), index=True)
    groceries = db.relationship('Grocery',
                                secondary=grocery_meal_map)
    menus = db.relationship('Menu',
                            secondary=meal_menu_map,
                            back_populates='meals')

    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            '_links': {
                'self': url_for('api.get_meal', user_id=self.user.id, id=self.id),
                'user': url_for('api.get_user', id=self.user.id),
                'menus': '<menus>',
                'groceries': '<groceries>'
            }
        }
        return data

    def __repr__(self):
        # TODO: maybe return a jsonify'd dictionary?
        return "<Meal: {},\n name: {},\n user_id: {}>".format(self.id, self.name, self.user_id)

    def add_to_menu(self, menu):
        self.menus.append(menu)
        db.session.add(menu)
        db.session.add(self)
        db.session.commit()

class Menu(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'))
    name = db.Column(db.String(60), default="Menu for {}".format(date.today()))
    date = db.Column(db.DateTime, index=True)
    meals = db.relationship('Meal',
                            secondary=meal_menu_map,
                            back_populates='menus')

    def add_meal(self, meal):
        self.meals.append(meal)
        db.session.add(meal)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        data = {
            'id':self.id,
            'user_id': self.user_id,
            'name': self.name,
            'date': self.date,
            '_links': {
                'self': url_for('api.get_menu', user_id=self.user.id, id=self.id),
                'user': url_for('api.get_user', id=self.user_id),
                'groceries': '<groceries>',
                'meals': '<meals>',
            }
        }
        return data

    def __repr__(self):
        # TODO: maybe return a jsonify'd dictionary?
        return "<Meal: {},\n user_id: {},\n name: {}\n date: {}>".format(self.id,
                                                                          self.user_id,
                                                                          self.name,
                                                                          self.date)

class Store(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'))
    name = db.Column(db.String(60))
    groceries = db.relationship('Grocery',
                                backref='store', lazy='dynamic')

    def add_grocery(self, grocery):
        self.groceries.append(grocery)
        db.session.add(meal)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            '_links': {
                'self': url_for('api.get_meal', user_id=self.user.id, id=self.id),
                'user': url_for('api.get_user', id=self.user.id),
                'groceries': '<groceries>'
            }
        }
        return data

    def __repr__(self):
        # TODO: maybe return a jsonify'd dictionary?
        return "<Store: {},\n name: {}, user_id: {}>".format(self.id, self.name, self.user_id)
