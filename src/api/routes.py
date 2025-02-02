"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Traveler, House, Feedback
from api.utils import generate_sitemap, APIException
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash


api = Flask(__name__)
api = Blueprint('api', __name__)


# ENDPOINT REGISTRO VIAJERO
@api.route('/register', methods=['POST'])
def register_user():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'userName' not in body:
        raise APIException('You need to specify the userName', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)

    # Check if the email already exists
    existing_traveler = Traveler.query.filter_by(email=body['email']).first()
    if existing_traveler:
        return jsonify({"message": "Email already in use"}), 409  

    try:
        # Create a new Traveler instance
        hashed_password = generate_password_hash(body['password'])
        new_traveler = Traveler(userName=body['userName'], email=body['email'], password=hashed_password)
        db.session.add(new_traveler)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201  
    except IntegrityError:
        db.session.rollback()  
        return jsonify({"message": "An error occurred during registration"}), 500  

# Autenticación de usuarios para obtener el token JWT

@api.route('/login', methods=['POST'])
def login():
    body = request.get_json()

    if 'email' not in body or 'password' not in body:
        return jsonify({"msg": "You need to specify the email and password"}), 400

    traveler = Traveler.query.filter_by(email=body['email']).first()

    if traveler is None or not check_password_hash(traveler.password, body['password']):
        return jsonify({"msg": "Bad username or password"}), 401
    
    if traveler is None or not check_password_hash(traveler.password, body['password']):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=traveler.id)
    return jsonify(access_token=access_token), 200


# ENDPOINT PROTEGIDO VIAJERO

@api.route('/traveler/profile', methods=['GET'])
@jwt_required()
def get_traveler_profile():
    current_traveler_id = get_jwt_identity()
    current_traveler = Traveler.query.get(current_traveler_id)

    # if current_traveler.role != 'Traveler':
    #     return jsonify({'message': 'Cannot perform that function!'}), 403

     # ^^ ESTE SERIA INTERESANTE COMO FEATURE ADICIONAL, PARA DIFERENCIAR LOS TIPOS DE USUARIOS CON DIFERENTES FUNCIONALIDADES O ACCESOS. EJ. TRAVELER, PROVEEDOR, ADMIN. TOCARIA AGREGARLO EN EL MODELO^^ 

    profile = {
        "userName": current_traveler.userName,
        "email": current_traveler.email,
        # "joined_date": current_traveler.joined_date

        # ^^ ESTE SERIA INTERESANTE COMO FEATURE ADICIONAL, TOCARIA AGREGARLO EN EL MODELO^^ 
    }

    return jsonify(profile)



# ENDPOINT CREAR CASAS RURALES
@api.route('/houses', methods=['POST'])
@jwt_required()
def create_house():
    body = request.get_json()

    if not body:
        return jsonify({"msg": "Invalid JSON"}), 400

    new_house = House(
        name=body.get('name'),
        address=body.get('address'),
        type=body.get('type'),
        image1=body.get('image1'),
        image2=body.get('image2'),
        image3=body.get('image3'),
        image4=body.get('image4')
    )
    db.session.add(new_house)
    db.session.commit()

    return jsonify({"msg": "House created successfully", "house": new_house.serialize()}), 201



# ENDPOINT MOSTRAR CASAS RURALES DISPONIBLES

@api.route('/houses', methods=['GET'])
def get_all_houses():
    houses = House.query.all()
    houses_list = [house.serialize() for house in houses]
    return jsonify(houses_list), 200


# ENDPOINT CASAS RURALES POR ID

@api.route('/houses/<int:id>', methods=['GET'])
def get_house(id):
    house = House.query.get(id)

    if not house:
        return jsonify({"msg": "House not found"}), 404

    return jsonify(house.serialize()), 200

# ENDPOINT PARA ACTUALIZAR/EDITAR DATOS DE CASAS RURALES 

@api.route('/houses/<int:id>', methods=['PUT'])
@jwt_required()
def update_house(id):
    body = request.get_json()

    house = House.query.get(id)

    if not house:
        return jsonify({"msg": "House not found"}), 404

    house.name = body.get('name', house.name)
    house.address = body.get('address', house.address)
    house.type = body.get('type', house.type)
    house.image1 = body.get('image1', house.image1)
    house.image2 = body.get('image2', house.image2)
    house.image3 = body.get('image3', house.image3)
    house.image4 = body.get('image4', house.image4)

    db.session.commit()

    return jsonify({"msg": "House updated successfully", "house": house.serialize()}), 200


# ENDPOINT PARA ELIMINAR CASAS RURALES 

@api.route('/houses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_house(id):
    house = House.query.get(id)

    if not house:
        return jsonify({"msg": "House not found"}), 404

    db.session.delete(house)
    db.session.commit()

    return jsonify({"msg": "House deleted successfully"}), 200



# ENDPOINT PARA VER DETTALES ADICIONALES/ INFORMACION SENSIBLE: DESCRIPTION, PPN, AVAILABILITY, CONTACT INFO, SPECIFIC ADDRESS. SE NECESITARIA AGREGAR DATOS EN EL MODELO. 

# @api.route('/houses/<int:id>/details', methods=['GET'])
# @jwt_required()
# def get_house_details(house_id):
#     house = House.query.get(house_id)
#     if house is None:
#         return jsonify({"msg": "House not found"}), 404
    
#     return jsonify(house.serialize_details()), 200

@api.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    new_feedback = Feedback(
        name=data['name'],
        email=data['email'],
        ratings=data['ratings'],
        message=data.get('message')
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({"message": "Feedback submitted successfully!"}), 201







