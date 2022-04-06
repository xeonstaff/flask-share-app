from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Item, item_schema, items_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}


@api.route('/data')
def viewdata():
    data = get_item()
    response = jsonify(data)
    print(response)
    return render_template('index.html', data=data)


@api.route('/items', methods=['POST'])
@token_required
def create_item(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    item = item(name, email, phone_number,
                      address, user_token=user_token)

    db.session.add(item)
    db.session.commit()

    response = item_schema.dump(item)
    return jsonify(response)


@api.route('/items', methods=['GET'])
@token_required
def get_item(current_user_token):
    a_user = current_user_token.token
    items = item.query.filter_by(user_token=a_user).all()
    response = items_schema.dump(items)
    return jsonify(response)


@api.route('/items/<id>', methods=['GET'])
@token_required
def get_single_item(current_user_token, id):
    item = item.query.get(id)
    response = item_schema.dump(item)
    return jsonify(response)

# UPDATE endpoint


@api.route('/items/<id>', methods=['POST', 'PUT'])
@token_required
def update_item(current_user_token, id):
    item = item.query.get(id)
    item.name = request.json['name']
    item.email = request.json['email']
    item.phone_number = request.json['phone_number']
    item.address = request.json['address']
    item.user_token = current_user_token.token

    db.session.commit()
    response = item_schema.dump(item)
    return jsonify(response)


@api.route('/items/<id>', methods=['DELETE'])
@token_required
def delete_item(current_user_token, id):
    item = item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    response = item_schema.dump(item)
    return jsonify(response)
