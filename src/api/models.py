from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


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
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<Admin {self.id} name: {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'name': self.name,
                'is_active': self.is_active}   
                  

    def serialize_public(self):
        return {'admin_name': self.name}  


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))  
    name = db.Column(db.String(120), unique=True, nullable=False)   
    address = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.Integer)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)   
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
                'is_active': self.is_active,   
                'id_type': self.id_type,
                'id_number': self.id_number}   


class Films(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    director = db.Column(db.String(120))
    description = db.Column(db.String(800))

    def __repr__(self):
        return f'<Films {self.id} name: {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'director': self.director,
                'description': self.description}   


class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    film_id = db.Column(db.String(120), db.ForeignKey('films.id'))
    country = db.Column(db.String(120), nullable=False)
    img_url = db.Column(db.String(120))  

    def __repr__(self):
        return f'Places {self.id} country: {self.country}>'

    def serialize(self):
        return {'id': self.id,
                'title': self.title,
                'film_id': self.film_id,
                'country': self.country,
                'img_url': self.img_url}                       


class Travels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    days = db.Column(db.Integer)
    price = db.Column(db.Integer)
    description = db.Column(db.String(500), nullable=False)
    place_id = db.Column(db.String(120), db.ForeignKey('places.id'))
    img_url = db.Column(db.String)
    itinerary = db.Column(db.String)

    def __repr__(self):
        return f'<Travels {self.id} name: {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'days': self.days,
                'price': self.price,
                'description': self.description,
                'place_id': self.place_id,
                'img_url': self.img_url,
                'itinerary': self.itinerary}    


class Departures(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    travel_id = db.Column(db.Integer, db.ForeignKey('travels.id'))
    dates = db.Column(db.Integer)
    coordinator_name = db.Column(db.String)
    coordinator_img = db.Column(db.String)

    def __repr__(self):
        return f'<Departures {self.id}>'

    def serialize(self):
        return {'id': self.id,
                'travel_id': self.travel_id,
                'dates': self.dates,
                'coordinator_name': self.coordinator_name,
                'coordinator_img': self.coordinator_img}


class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure_id = db.Column(db.Integer, db.ForeignKey('departures.id'))   
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    payment = db.Column(db.Integer)
    price = db.Column(db.Integer)
    passengers = db.Column(db.Integer)

    def __repr__(self):
        return f'<ShoppingCart {self.id}>'

    def serialize(self):
        return {'id': self.id,
                'departure_id': self.departure_id,
                'customer_id': self.customer_id,
                'payment': self.payment,
                'price': self.price,
                'passengers': self.passengers}                    
