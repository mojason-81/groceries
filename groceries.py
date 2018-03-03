from app import app, db
from app.models import User, Grocery, Store, Menu, Meal

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Grocery': Grocery,
            'Store': Store,
            'Menu': Menu,
            'Meal': Meal}
