import logging
from http import HTTPStatus

from flask import jsonify, request

from app import db
from app.models import Product, User
from app.products.client import get_product_by_id
from app.products.exceptions import ProductHttpException


def create_user() -> tuple:
    data = request.get_json()

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


def update_user(current_user: User, id: int) -> tuple:
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


def get_user(id: int) -> tuple:
    user = User.query.get(id)
    if user:
        return jsonify(
            {
                'message': 'successfully fetched',
                'data': user.as_dict()
            }
        ), HTTPStatus.OK
    return jsonify({'message': 'user not found'}), HTTPStatus.NOT_FOUND


def get_users() -> tuple:
    users = User.query.all()
    if users:
        return jsonify(
            {
                'message': 'success',
                'users': [user.as_dict() for user in users]
            }
        ), HTTPStatus.OK
    return jsonify({'message': 'no users'}), HTTPStatus.OK


def delete_user(current_user: User, id: int) -> tuple:
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
        return jsonify(
            {
                'message': 'successfully deleted'
            }
        ), HTTPStatus.ACCEPTED
    except Exception:
        return jsonify(
            {
                'message': 'unable to delete'
            }
        ), HTTPStatus.INTERNAL_SERVER_ERROR


def remove_product(current_user: User, product_id: str) -> tuple:
    product = Product.query.filter(
        Product.user.has(id=current_user.id),
        product_id == product_id).first()
    if product:
        current_user.products.remove(product)
        db.session.commit()
        return jsonify(
            {
                'message': 'product removed from list'
            }
        ), HTTPStatus.ACCEPTED

    return jsonify(
        {
            'message': 'product not found in list'
        }
    ), HTTPStatus.NOT_FOUND


def get_product(current_user: User, product_id: str) -> tuple:
    try:
        exists_product = Product.query.filter_by(product_id=product_id).first()

        if not exists_product:
            product = get_product_by_id(product_id)

            if product:
                p = Product()
                p.from_dict(product)
                p.product_id = product_id
                current_user.products.append(p)
                db.session.commit()
                return jsonify(
                    {
                        'message': 'product added in list'
                    }
                ), HTTPStatus.OK

        if exists_product in current_user.products:
            return jsonify(
                {
                    'message': 'product already in list'
                }
            ), HTTPStatus.OK

        current_user.products.append(exists_product)
        db.session.commit()
        return jsonify({'message': 'product added in list'}), HTTPStatus.OK
    except ProductHttpException as exc:
        raise exc.args[0]
