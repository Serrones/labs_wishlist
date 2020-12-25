from app.models import Product, User
from app.products.client import get_product_by_id

import logging
from http import HTTPStatus

from flask import jsonify, request
from app import db


def create_user():
    data = data = request.get_json()

    fields = ['email', 'username', 'password', 'is_admin']

    for field in fields:
        if field not in data:
            logging.warning('User not created -- Missing field')
            return jsonify(
                {
                    'Error': 'Missing field ' + field
                }
            ), HTTPStatus.BAD_REQUEST
    
    user_exists = User.query.filter(User.username == data['username']).first()

    if user_exists:
        logging.warning(
            'User not created -- There is an User with this username'
        )
        return jsonify(
            {
                'Error': 'Already exists user with this username'
            }
        ), HTTPStatus.FORBIDDEN

    user = User()
    user.from_dict(data)
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    logging.info(
        f'User {user.username} created.'
    )
    return jsonify(
        {
            'message': 'User created',
            'data': user.as_dict()
        }
    ), HTTPStatus.CREATED


def update_user(current_user, id):
    if not current_user.is_admin:
        return jsonify(
            {'message': 'you dont have permission'}
        ), HTTPStatus.UNAUTHORIZED

    data = request.get_json()

    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'user doesnt exists'}), HTTPStatus.NOT_FOUND

    fields = ['email', 'username', 'password', 'is_admin']

    for field in data:
        if field not in fields:
            logging.warning('User not updated -- Invalid field')
            return jsonify({'Error': 'Invalid field'}), HTTPStatus.BAD_REQUEST

    user.from_dict(data)

    if 'passowrd' in data:
        user.set_password(data['password'])
    
    db.session.commit()

    return jsonify(
        {
            'message': 'successfully updated',
            'data': user.as_dict()
        }
    ), HTTPStatus.CREATED


def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(
            {
                'message': 'successfully fetched',
                'data': user.as_dict()
            }
        ), HTTPStatus.OK
    return jsonify({'message': 'user not found'}), HTTPStatus.NOT_FOUND


def get_users():
    users = User.query.all()
    if users:
        return jsonify(
            {
                'message': 'success',
                'users': [user.as_dict() for user in users]
            }
        ), HTTPStatus.OK
    return jsonify({'message': 'no users'}), HTTPStatus.OK


def delete_user(current_user, id):
    if not current_user.is_admin:
        return jsonify(
            {'message': 'you dont have permission'}
        ), HTTPStatus.UNAUTHORIZED

    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'user not found'}), HTTPStatus.NOT_FOUND

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'successfully deleted'}), HTTPStatus.ACCEPTED
    except Exception:
        return jsonify(
            {
                'message': 'unable to delete'
            }
        ), HTTPStatus.INTERNAL_SERVER_ERROR
