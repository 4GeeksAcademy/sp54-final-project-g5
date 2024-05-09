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
        return {'id': self.id,
                'email': self.email,
                'is_active': self.is_active}

    def serialize_public(self):
        return {'user_email': self.email}        


class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_to = db.relationship('Users', foreign_keys=[user_id])

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
    name = db.Column(db.String(120), unique=True, nullable=False)   
    address = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.Integer)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)   
    id_type = db.Column(db.Integer)
    id_number = db.Column(db.Integer)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_to = db.relationship('Users', foreign_keys=[user_id]) 

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

    def serialize_public(self):
        return {'customer_name': self.name,
                'customer_address': self.address,
                'customer_phone': self.phone,
                'customer_id_type': self.id_type,
                'customer_id_number': self.id_number}              


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

    def serialize_public(self):
        return {'film_name': self.name,
                'director': self.director,
                'film_description': self.description}            


class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    img_url = db.Column(db.String(120)) 
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))
    film_to = db.relationship('Films', foreign_keys=[film_id]) 

    def __repr__(self):
        return f'Places {self.id} country: {self.country}>'

    def serialize(self):
        return {'id': self.id,
                'title': self.title,
                'film_id': self.film_id,
                'country': self.country,
                'img_url': self.img_url}   

    def serialize_public(self):
        return {'title': self.title,
                'country': self.country,
                'place_img_url': self.img_url}                                


class Travels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    days = db.Column(db.Integer)
    price = db.Column(db.Integer)
    description = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String)
    itinerary = db.Column(db.String)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    place_to = db.relationship('Places', foreign_keys=[place_id])

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

    def serialize_public(self):
        return {'travel_name': self.name,
                'days': self.days,
                'price': self.price,
                'travel_description': self.description,
                'travel_img_url': self.img_url,
                'itinerary': self.itinerary}
                                

class Departures(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    dates = db.Column(db.Integer)
    coordinator_name = db.Column(db.String)
    coordinator_img = db.Column(db.String)
    travel_id = db.Column(db.Integer, db.ForeignKey('travels.id'))
    travel_to = db.relationship('Travels', foreign_keys=[travel_id])

    def __repr__(self):
        return f'<Departures {self.id}>'

    def serialize(self):
        return {'id': self.id,
                'travel_id': self.travel_id,
                'dates': self.dates,
                'coordinator_name': self.coordinator_name,
                'coordinator_img': self.coordinator_img}

    def serialize_public(self):
        return {'dates': self.dates,
                'coordinator_name': self.coordinator_name,
                'coordinator_img': self.coordinator_img}


class Carts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment = db.Column(db.Integer)
    price = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    departure_id = db.Column(db.Integer, db.ForeignKey('departures.id'))   
    departure_to = db.relationship('Departures', foreign_keys=[departure_id])
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer_to = db.relationship('Customers', foreign_keys=[customer_id])

    def __repr__(self):
        return f'<ShoppingCart {self.id}>'

    def serialize(self):
        return {'id': self.id,
                'departure_id': self.departure_id,
                'customer_id': self.customer_id,
                'payment': self.payment,
                'price': self.price,
                'passengers': self.passengers} 

    def serialize_public(self):
        return {'payment': self.payment,
                'price': self.price,
                'passengers': self.passengers}
                                                   