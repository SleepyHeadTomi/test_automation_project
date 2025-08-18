from flask import Blueprint, jsonify, request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models import db, User

routes = Blueprint('routes', __name__)

@routes.route('/users', methods=['GET'])
def get_users():
    stmt = select(User)
    users = db.session.scalars(stmt).all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@routes.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)

    if user is None:
        return jsonify({'error': 'User not found!'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

@routes.route('/users', methods=['POST'])
def post_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Missing name or email.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'E-mail already exists!'}), 409

    new_user = User(name=name, email=email)

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 500

    return jsonify({'message': 'User added!', 'id': new_user.id}), 201

@routes.route('/users/<int:id>', methods=['DELETE'])
def del_user(id):
    user = db.session.get(User, id)

    if user is None:
        return jsonify({'error': 'User not found!'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User with id {id} deleted.'}), 200

@routes.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)

    if user is None:
        return jsonify({'error': 'User not found!'}), 404

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Missing name or e-mail.'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.id != user.id:
        return jsonify({'error': 'E-mail already exists.'}), 409


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

@routes.route('/users/all', methods=['DELETE'])
def delete_all_users():
    try:
        num_rows_deleted = db.session.query(User).delete()
        db.session.commit()
        return jsonify({'message': f'{num_rows_deleted} users deleted.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Could not delete users'}), 500