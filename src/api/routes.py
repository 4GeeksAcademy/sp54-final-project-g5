"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, Admins, Customers, Films, Places, Travels, Departures, ShoppingCart


api = Blueprint('api', __name__)
CORS(api)  # Allow CORS requests to this API


@api.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {}
    response_body['message'] = "Hello! I'm a message that came from the backend"
    return response_body, 200

@api.route('/register', methods=['POST'])
def handle_register():
    response_body = {}
    response_body['message'] = "Hello! You are registered"
    return response_body, 200    

""" @api.route('/login', methods=['GET'])
def handle_login():
    response_body = {}
    response_body['message'] = "Login!!"
    return response_body, 200   """

@api.route("/login", methods=["POST"])
def handle_login():
    data = request.get_json()
    email = data.get("email", None)
    email = email.lower() if email else None
    password = data.get("password", None)
    # remember_me = request.json.get("remember_me", False)
    user = db.one_or_404(db.select(Users).filter_by(email=email, password=password, is_active=True),
                         description=f"Bad email or password.")
    results = {'user': user.serialize(),
               'admin': None,
               'customer': None}           
    admin = db.session.execute(db.select(Admins).where(Admins.user_id == user.id)).scalar()
    if admin:
        results['admin'] = admin.serialize()
        customer = db.session.execute(db.select(Customers).where(Customers.user_id == user.id)).scalar()
        results['customer'] = customer.serialize() if customer else None
    access_token = create_access_token(identity=[user.id,
                                                 user.is_admin,
                                                 admin.id if results['admin'] else None,
                                                 customer.id if results['customer'] else None])                                              
    response_body = {'message': 'Token created',
                     'token': access_token,
                     'results': results}
    return response_body, 200


@api.route('/users', methods=['GET'])  # El POST se realiza en /login
@jwt_required() 
def handle_users():
    identity = get_jwt_identity()
    # Valido si es admin
    if identity[1]:
        users = db.session.execute(db.select(Users)).scalars()
        users_list = [user.serialize() for user in users]
        response_body = {'message': 'User List', 
                         'results': users_list}
        return response_body, 200 
    response_body = {'message': "Restricted access"}
    return response_body, 401


@api.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required() 
def handle_user_id(user_id):
    identity = get_jwt_identity()
    # Valido si es admin
    if identity[1]:
        user = db.one_or_404(db.select(Users).filter_by(id=user_id), 
                             description=f"User not found , 404.")
        if request.method == 'GET':
            response_body = {'message': 'User', 
                             'results': user.serialize()}
            return response_body, 200
        if request.method == 'PUT':
            data = request.get_json()
            user.email = data['email']
            user.password = data['password']
            user.is_active = data['is_active']
            user.is_admin = data['is_admin']
            db.session.commit()
            response_body = {'message': 'User updated', 
                             'results': user.serialize()}
            return response_body, 200
        if request.method == 'DELETE':
            user.is_active = False
            db.session.commit()
            response_body = {'message': 'User inactived'}
            return response_body, 200
    response_body = {'message': "Restricted access"}
    return response_body, 401
       
    
@api.route('/customers', methods=['GET'])  # El POST se realiza en /signup
def handle_customers():
    customers = db.session.execute(db.select(Customers).where(Customers.is_active)).scalars()
    response_body = {'message': 'Customers', 
                     'results': Customers}
    return response_body, 200 
   

@api.route('/customers/<int:customers_id>', methods=['GET'])
def handle_get_customer_id(customer_id):
    customer = db.one_or_404(db.select(Customer).filter_by(id=customer_id), 
                           description=f"Customer not found , 404.")
    response_body = {'message': 'Customers', 
                     'results': customer.serialize()}
    return response_body, 200
  

@api.route('/customers/<int:customers_id>', methods=['PUT', 'DELETE'])
@jwt_required() 
def handle_customers_id(customers_id):
    identity = get_jwt_identity()  # Aquí llega el token
    # Valido si es admin o author:
    if identity[1] or identity[2] == customers_id:
        customer = db.one_or_404(db.select(Customers).filter_by(id=customer_id), 
                               description=f"Customer not found , 404.")
        if request.method == 'PUT':
            data = request.get_json()
            customer.name = data['name']
            customer.address = data['address']
            customer.phone = data['phone']
            customer.is_active = data['is_active']
            customer.id_type = data['id_type']
            customer.id_number = data['id_number']
            db.session.commit()
            response_body = {'message': 'Customer updated', 
                             'results': customer.serialize()}
            return response_body, 200
        if request.method == 'DELETE':
            customer.is_active = False
            db.session.commit()
            response_body = {'message': 'Customer inactived'}
            return response_body, 200
    response_body = {'message': "Restricted access"}
    return response_body, 401
    
    
@api.route('/admins', methods=['GET']) 
def handle_get_admins():
        admins = db.session.execute(db.select(Admins).where(Admins.is_active)).scalars()
        members_list = [member.serialize() for member in members]
        response_body = {'message': 'Admins', 
                         'results': admins_list}
        return response_body, 200 
    

@api.route('/admins/<int:admin_id>', methods=['GET'])
def handle_get_admin_id(member_id):
    admin = db.one_or_404(db.select(Admin).filter_by(id=admin_id), 
                           description=f"Member not found , 404.")
    response_body = {'message': 'Admin', 
                     'results': admin.serialize()}
    return response_body, 200


@api.route('/admin/<int:member_id>', methods=['PUT', 'DELETE'])
@jwt_required() 
def handle_admin_id(admin_id):
    identity = get_jwt_identity()
    if not identity[1] and not identity[3]:
        response_body = {'message': "Restricted access"}
        return response_body, 401
    admin = db.one_or_404(db.select(Admin).filter_by(id=admin_id), 
                           description=f"Admin not found , 404.")
    # Valido si es admin o author:
    if request.method == 'PUT' and identity[1] == admin.id:
        admin.name = data['name']
        admin.is_active = data['is_active']
        db.session.commit()
        response_body = {'message': 'Admin updated', 
                         'results': admin.serialize()}
        return response_body, 200
    if request.method == 'DELETE':
        admin.is_active = False
        db.session.commit()
        response_body = {'message': 'Admin inactived'}
        return response_body, 200

@api.route('/travels', methods=['GET'])
def handle_travels():
    # Obtiene los viajes de la base de datos
    travels = Travels.query.all()

    serialized_travels = []
    for travel in travels:
        serialized_travel = {
            'id': travel.id,
            'name': travel.name,
            'days': travel.days,
            'price': travel.price,
            'description': travel.description,
            'place_id': travel.place_id,
            'img_url': travel.img_url,
            'itinerary': travel.itinerary
        }
        serialized_travels.append(serialized_travel)

    # Devuelve el listado de travels.
    return jsonify({'travels': serialized_travels}), 200

@api.route('/places', methods=['GET'])
def handle_places():
    # Implementa la lógica para obtener los lugares y devolverlos como respuesta
    return jsonify({'message': 'Places endpoint'})

@api.route('/films', methods=['GET'])
def handle_films():
    # Implementa la lógica para obtener las películas y devolverlas como respuesta
    return jsonify({'message': 'Films endpoint'})

@api.route('/departures', methods=['GET'])
def handle_departures():
    # Implementa la lógica para obtener las salidas y devolverlas como respuesta
    return jsonify({'message': 'Departures endpoint'})

@api.route('/shopping-cart', methods= ['GET', 'POST'])
def handle_shopping_cart():
    if request.method == 'GET':
        # Implementa la lógica para obtener el carrito de compras y devolverlo como respuesta
        return jsonify({'message': 'Shopping Cart GET endpoint'})
    elif request.method == 'POST':
        # Implementa la lógica para agregar elementos al carrito de compras
        # Aquí puedes acceder a los datos del carrito desde request.json
        return jsonify({'message': 'Shopping Cart POST endpoint'})

# @api.route('/payment')

