import token
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Service, service_schema, services_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/services', methods = ['POST'])
@token_required
def create_service(current_user_token):
    vehicle = request.json['vehicle']
    service_date = request.json['service_date']
    description = request.json['description']
    mileage = request.json['mileage']
    notes = request.json['notes']
    cost = request.json['cost']
    follow_up = request.json['follow_up']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    service = Service(vehicle, service_date, description, mileage, notes, cost, follow_up, user_token = user_token)

    db.session.add(service)
    db.session.commit()

    response = service_schema.dump(service)
    return jsonify(response)

@api.route('/services', methods = ['GET'])
@token_required
def get_service_history(current_user_token):
    a_user = current_user_token.token
    services = Service.query.filter_by(user_token = a_user).all()
    response = services_schema.dump(services)
    return jsonify(response)

@api.route('/services/<id>', methods=['GET'])
@token_required
def get_single_service(current_user_token, id):
    service = Service.query.get(id)
    response = service_schema.dump(service)
    return jsonify(response)

@api.route('/services/<id>', methods = ['DELETE'])
@token_required
def delete_service(current_user_token, id):
    service = Service.query.get(id)
    db.session.delete(service)
    db.session.commit()
    response = service_schema.dump(service)
    return jsonify(response)