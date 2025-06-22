from flask import Blueprint, jsonify, request
from models import db, User

routes = Blueprint('routes', __name__)

@routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@routes.route('/users', methods=['POST'])
def post_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Missing name or email'}), 400

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added', 'id': new_user.id}), 201

@routes.route('/users/<int:id>', methods=['DELETE'])
def del_user(id_):
    user = User.query.get(id)

    if user is None:
        return jsonify({'error': 'User not found!'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User with id {id} deleted.'}), 200

@routes.route('/users/<int:id>', methods=['PUT'])
def update_user(id_):
    user = User.query.get(id)

    if user is None:
        return jsonify({'error': 'User not found!'}), 404

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    user.name = name
    user.email = email

    db.session.commit()

    return jsonify({'message': f'User updated successfully!',
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email
                    }
                }), 200