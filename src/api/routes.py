"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, Admins, Customers, Films, Places, Travels, Departures, ShoppingCart
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies
from sqlalchemy import func 
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)
CORS(api)  # Allow CORS requests to this API


@api.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {}
    response_body['message'] = "Hello! I'm a message that came from the backend"
    return response_body, 200

@api.route('/register', methods=['GET'])
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

@api.route('/signup', methods=["POST"])
def handle_signup():
    data = request.get_json()
    response_body = {}
    try: 
        email = data['user']['email'].lower()
    except:
        response_body['message'] = 'user.email is empty or wrong'
        return response_body, 400
    # Verificamos si el usuario ya existe
    is_user = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
    if is_user:
        response_body['message'] = 'The email is registered'
        return response_body, 403
    # Almacenamos en memoria los datos de user y admin (member, se debe crear desde POST /member)
    data_user = data['user']
    data_admin = data.get('admin', None)
    # Si es admin, verificamos que no exista (por el name y el user_id)
    if data_admin:
        try:
            name = data['admin']['name'].lower()
            user_id = data['admin']['user_id']
        except:
            response_body['message'] = ' admin.name o admin.id  is empty or wrong'
            return response_body, 400
        is_name = db.session.execute(db.select(Admins).where(func.lower(Admins.name) == name)).scalar()
        is_user_id = db.session.execute(db.select(Admins).where(func.lower(Admins.user_id) == id)).scalar()
        if is_name or is_user_id:
            response_body['message'] = 'The name or nif is registered'
            return response_body, 403
    # Si la estructura del JSON es incorrecta, no se podrán cargar los datos
    try:
        user = Users(email=data_user['email'], 
                     password=data_user['password'], 
                     is_active=True)
        db.session.add(user)
        db.session.commit()
        results = {'user': user.serialize(),
                   'member': None,
                   'advis': None}
        if data_advisor:
            advisor = Admins(name=data_advisor['name'],  
                               is_active=True,
                               user_id=user.id)
            db.session.add(advisor)
            db.session.commit()
            results['admin'] = advisor.serialize()
        access_token = create_access_token(identity=[user.id,
                                                     None,
                                                     admin.id if data_admin else None])
        response_body = {'message': 'User created',
                         'token': access_token,
                         'results': results}
    except:
        response_body = {'message': "Bad JSON structure"}
        return response_body, 400
    return response_body, 201


@api.route('/logout', methods=["POST"])
@jwt_required()
def handle_logout():
    user_id = get_jwt_identity()[0]  # Obtén el ID del usuario a partir del token
    unset_jwt_cookies()  # Revoca el token actual para deshabilitarlo
    response_body = {'message': 'Logout successful'}
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
    travels = db.session.execute(db.select(Travels)).scalars()
    response_body = {'message': 'Travels', 
                     'results': Travels}
    return response_body, 200 

@api.route('/places', methods=['GET'])
def handle_places(): 
    places = db.session.execute(db.select(Places)).scalars()
    response_body = {'message': 'Places', 
                      'results': Places}
    return response_body, 200 


@api.route('/films', methods=['GET'])
def handle_films(): 
    films = db.session.execute(db.select(Films)).scalars()
    response_body = {'message': 'Films', 
                     'results': Films}
    return response_body, 200 

@api.route('/departures', methods=['GET'])
def handle_departures(): 
    departures = db.session.execute(db.select(Departures)).scalars()
    response_body = {'message': 'Departures', 
                     'results': Departures}
    return response_body, 200 

@api.route('/shoppingcart', methods= ['GET'])
@jwt_required()
def handle_shoppingcart():
    identity = get_jwt_identity()
    if request.method == 'GET' and identity[1]:
        carts = db.session.execute(db.select(ShoppingCart)).scalars()
        cart_list = [cart.serialize() for cart in carts]
        response_body = {'message': 'ShoppingCart',
                         'results': cart_list}
        return response_body, 200 

@api.route('/shoppingcart', methods= ['POST']) 
@jwt_required()
def handle_shoppingcart():
    identity = get_jwt_identity()
    if request.method == 'POST' and member_id:
        cart = db.session.execute(db.select(ShoppingCarts).where(ShoppingCarts.member_id == member_id)).scalar()
        results = {}
        if not cart:
            # Verificamos si ya tiene un carrito
            cart = ShoppingCart(price=
                                departure_id = 
                                customer_id = 
                                payment = 
                                passengers =)
            db.session.add(shoppingcart)
            db.session.commit()
        data = request.get_json()
        cart_item = ShoppingCart (price=data['price'],
                                  departure_id = data ['departures.id'],
                                  customer_id = data['customers.id'],
                                  payment = data ['payment'],
                                  passengers = data ['passengers'])
        db.session.add(shoppingcart)
        db.session.commit()
        # Actualizamos el monto total del carrito
        cart['payment'] += cart_item['price'] * cart_item['passengers']
        db.session.commit()
        results['shopping_cart'] = cart.serialize()
        cart_items = db.session.execute(db.select(ShoppingCart)).scalars()
        list_items = []
        for item in cart_items:
            list_items.append(item.serialize())
        results['shoppingcart'] = list_items
        response_body = {'message': 'Shopping Cart with all items', 
                         'results': results}
        return response_body, 201 
    response_body = {'message': "Restricted access"}
    return response_body, 401

# @api.route('/payment')

