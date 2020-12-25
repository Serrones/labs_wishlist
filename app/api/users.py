import logging
from http import HTTPStatus

from flask import jsonify, request

from app import db
from app.api import bp
from app.authentication import auth, token_required
from app.models import Product, User
from app.products.client import get_product_by_id


@bp.route('/auth', methods=['GET'])
def authenticate():
    return auth()


@bp.route('/users', methods=['POST'])
def create_user():
    data = data = request.get_json()
    user = User()
    user.from_dict(data)
    user.set_password(data['password'])

    try:
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
    except Exception:
        print(exc)
        return jsonify(
            {
                'message': 'Unable to create user'
            }
        ), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/users/<id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    if not current_user.is_admin:
        return jsonify(
            {'message': 'you dont have permission'}
        ), HTTPStatus.UNAUTHORIZED

    data = data = request.get_json()

    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'user doesnt exists'}), HTTPStatus.NOT_FOUND

    try:
        user.from_dict(data)
        user.set_password(password)
        db.session.commit()

        return jsonify(
            {
                'message': 'successfully updated',
                'data': user.as_dict()
            }
        ), HTTPStatus.CREATED

    except Exception:
        return jsonify(
            {
                'message': 'unable to update'
            }
        ), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/users/<id>', methods=['GET'])
@token_required
def get_user(current_user, id):
    user = User.query.get(id)
    if user:
        return jsonify(
            {
                'message': 'successfully fetched',
                'data': user.as_dict()
            }
        ), HTTPStatus.OK
    return jsonify({'message': 'user not found'}), HTTPStatus.NOT_FOUND


@bp.route('/users', methods=['GET'])
@token_required
def get_users(current_user):

    users = User.query.all()
    if users:
        return jsonify(
            {
                'message': 'success',
                'users': [user.as_dict() for user in users]
            }
        ), HTTPStatus.OK
    return jsonify({'message': 'no users'}), HTTPStatus.OK


@bp.route('/users/<id>', methods=['DELETE'])
@token_required
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
        return jsonify({'message': 'successfully deleted'}), HTTPStatus.OK
    except Exception:
        return jsonify(
            {
                'message': 'unable to delete'
            }
        ), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/users/list/<product_id>', methods=['GET'])
@token_required
def get_product(current_user, product_id):
    try:
        exists_product = Product.query.filter(product_id == product_id).first()

        if not exists_product:
            product = get_product_by_id(product_id)

            if product:
                p = Product()
                p.from_dict(product)
                p.product_id=product_id
                current_user.products.append(p)
                db.session.commit()
                return jsonify(
                    {
                        'message': 'product added in list'
                    }
                ), HTTPStatus.OK

        if exists_product in current_user.products:
            return jsonify({'message': 'product added in list'}), HTTPStatus.OK

        current_user.products.append(exists_product)
        db.session.commit()
        return jsonify({'message': 'product added in list'}), HTTPStatus.OK
    except Exception:
        return jsonify(
            {
                'message': 'An error as ocurred'
            }
        ), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/users/list/<product_id>', methods=['DELETE'])
@token_required
def remove_product(current_user, product_id):
    try:
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
            ), HTTPStatus.OK

        return jsonify(
            {
                'message': 'product not found in list'
            }
        ), HTTPStatus.NOT_FOUND

    except Exception:
        return jsonify(
            {
                'message': 'An error as ocurred'
            }
        ), HTTPStatus.INTERNAL_SERVER_ERROR
