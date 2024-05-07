import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, Users, Admins, Customers, Films, Places, Travels, Departures, Carts


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    # Add your models here, for example this is how we add a the Users model to the admin
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Admins, db.session))
    admin.add_view(ModelView(Customers, db.session))
    admin.add_view(ModelView(Films, db.session))
    admin.add_view(ModelView(Places, db.session))
    admin.add_view(ModelView(Travels, db.session))
    admin.add_view(ModelView(Departures, db.session))
    admin.add_view(ModelView(Carts, db.session))
