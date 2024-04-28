from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        # Do not serialize the password, its a security breach
        return {'id': self.id,
                'email': self.email,
                'is_active': self.is_active}

class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Admin {self.id} name: {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'name': self.name}  

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))  
    name = db.Column(db.String(120), unique=True, nullable=False)   
    address = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.Integer)   
    id_type = db.Column(db.Integer)
    id_number = db.Column(db.Integer)    

    def __repr__(self):
        return f'<Customers {self.id} name: {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'name': self.name,
                'address': self.address,
                'phone': self.phone,
                'id_type': self.id_type,
                'id_number': self.id_number}          