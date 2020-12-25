import logging
from http import HTTPStatus

from flask import jsonify, request

from app import db
from app.api import bp
from app.authentication import auth, token_required
from app.models import Product, User
from app.products.client import get_product_by_id

from app.views import (
    create_user,
    update_user,
    get_user,
    get_users,
    delete_user
)

@bp.route('/auth', methods=['GET'])
def authenticate():
    """
    @api {get} /auth
    Return Token
    @apiName authentication
    @apiGroup User

    @apiSuccess {Object} token 
    @apiSuccess {Date} token.exp Token expiration Date
    @apiSuccess {String} token.message Token message
    @apiSuccess {String} token.token Token

    @apiExample Request
        curl --location --request GET 'http://localhost:5000/api/auth' \
            --header 'Authorization: Basic bGluZGE6MTIzNDU2' \
            --data-raw ''

    @apiSuccessExample {json} Token
        HTTP/1.1 200 OK
        {
            "exp": "Sat, 26 Dec 2020 03:52:42 GMT",
            "message": "Validated sucessfully",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNlcnJvbmVzIiwiZXhwIjoxNjA4OTU0NzYyfQ.qhuNQ6ZCeNG6zSdF0DJpxTBUywbJI4UH4URZqXg7keM"
        }
    @apiError 401 User not found || login required
    """
    return auth()


@bp.route('/users', methods=['POST'])
def post_user():
    """
    @api {post} /users
    Create User
    @apiName create_user
    @apiGroup User

    @apiParam (Request body) {String} username Username
    @apiParam (Request body) {String} email Email
    @apiParam (Request body) {String} password Password
    @apiParam (Request body) {Booelan} is_admin Admin Permission

    @apiExample Request
        curl --location --request POST 'http://localhost:5000/api/users' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "username": "dona",
            "email": "dona@email.com",
            "password": "123456",
            "is_admin": false
        }'

    @apiSuccess {Object} oret User created
        HTTP/1.1 201 Created

    @apiSuccessExample {json} User
        HTTP/1.1 201 OK
        {
            "data": {
                "email": "dona@email.com",
                "id": 3,
                "is_admin": false,
                "products": [],
                "username": "dona"
            },
            "message": "User created"
        }
    @apiError 400 Missing Field
    @apiError 403 User already exists
    """
    return create_user()


@bp.route('/users/<id>', methods=['PUT'])
@token_required
def put_user(current_user, id):
    """
    @api {put} /user/:id_user
    Update User
    @apiName update_user
    @apiGroup User

    @apiHeader {String} x-access Authorization Token
    
    @apiParam {Number} id_user User ID

    @apiParam (Request body) {String} [username] Username
    @apiParam (Request body) {String} [email] Email
    @apiParam (Request body) {String} [password] Password
    @apiParam (Request body) {Booelan} [is_admin] Admin Permission

    @apiExample Request
        curl --location --request PUT 'http://localhost:5000/api/users/2' \
        --header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJlbGEiLCJleHAiOjE2MDg5NDcyMzB9.7NizIQC5MohaZZ2kt1PtvWBAa4wQMF8L6MuLk7jrv94' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "username": "serrones",
            "email": "serrones@mail.com",
            "password": "123456",
            "is_admin": false
        }'

    @apiSuccess {Object} oret User updated
        HTTP/1.1 200 Ok
    
    @apiSuccessExample {json} User
        HTTP/1.1 200 OK
        {
            "data": {
                "email": "serrones@mail.com",
                "id": 2,
                "is_admin": false,
                "products": [],
                "username": "serrones"
            },
            "message": "successfully updated"
        }
    @apiError 400 Invalid Field
    @apiError 401 Token missing || missing admin permission
    @apiError 404 User not found
    """
    return update_user(current_user, id)


@bp.route('/users/<id>', methods=['GET'])
@token_required
def fetch_user(current_user, id):
    """
    @api {get} /users/:id_user
    Get User
    @apiName get_user
    @apiGroup User

    @apiHeader {String} x-access Authorization Token

    @apiParam {Number} id_user User ID

    @apiSuccess {Object} user 
    @apiSuccess {String} user.data.email User Email
    @apiSuccess {String} user.data.id User id
    @apiSuccess {String} user.data.username User username
    @apiSuccess {Booelan} user.data.is_admin User admin permission
    @apiSuccess {List} user.data.products User products list
    @apiSuccess {String} user.message Success Message


    @apiExample Request
        HTTP/1.1 200 OK
        curl --location --request GET 'http://localhost:5000/api/users/1' \
            --header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJlbGEiLCJleHAiOjE2MDg5NDcyMzB9.7NizIQC5MohaZZ2kt1PtvWBAa4wQMF8L6MuLk7jrv94'

    @apiSuccess {Object} oret User fetched
        HTTP/1.1 200 Ok
    
    @apiSuccessExample {json} User
        HTTP/1.1 200 OK
        {
            "data": {
                "email": "bela@email.com",
                "id": 1,
                "is_admin": true,
                "products": [],
                "username": "bela"
            },
            "message": "successfully fetched"
        }
    @apiError 401 User not found || token missing
    """
    return get_user(id)


@bp.route('/users', methods=['GET'])
@token_required
def fetch_users(current_user):
    """
    @api {get} /users
    Get Users
    @apiName get_users
    @apiGroup User

    @apiHeader {String} x-access Authorization Token

    @apiSuccess {Object[]} list_users
    @apiSuccess {String} list_users.users.data.email User Email
    @apiSuccess {String} list_users.users.data.id User id
    @apiSuccess {String} list_users.users.data.username User username
    @apiSuccess {Booelan} list_users.users.data.is_admin User admin permission
    @apiSuccess {List} list_users.users.data.products User products list
    @apiSuccess {String} list_users.message Success Message


    @apiExample Request
        HTTP/1.1 200 OK
        curl --location --request GET 'http://localhost:5000/api/users' \
            --header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJlbGEiLCJleHAiOjE2MDg5NDcyMzB9.7NizIQC5MohaZZ2kt1PtvWBAa4wQMF8L6MuLk7jrv94'
    
    @apiSuccess {Object} oret Users fetched
        HTTP/1.1 200 Ok
    
    @apiSuccessExample {json} Users
        HTTP/1.1 200 OK
        {
            "message": "success",
            "users": [
                {
                    "email": "bela@email.com",
                    "id": 1,
                    "is_admin": true,
                    "products": [],
                    "username": "bela"
                },
                {
                    "email": "serrones@mail.com",
                    "id": 2,
                    "is_admin": true,
                    "products": [
                        {
                            "brand": "bébé confort",
                            "id": 1,
                            "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
                            "price": 1699.0,
                            "product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
                            "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown"
                        }
                    ],
                    "username": "serrones"
                }
            ]
        }
    @apiError 401 Token missing
    """
    return get_users()


@bp.route('/users/<id>', methods=['DELETE'])
@token_required
def del_user(current_user, id):
    """
    @api {delete} /users/:id_user
    Delete User
    @apiName delete_user
    @apiGroup User

    @apiHeader {String} x-access Authorization Token

    @apiParam {Number} id_user User ID

    @apiExample Request
        curl --location --request DELETE 'http://localhost:5000/api/users/2' \
            --header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJlbGEiLCJleHAiOjE2MDg5NDcyMzB9.7NizIQC5MohaZZ2kt1PtvWBAa4wQMF8L6MuLk7jrv94'

    @apiSuccess {json} User Deleted
        HTTP/1.1 202

    @apiSuccessExample {json} User deleted
        {
            "message": "successfully deleted"
        }

    @apiError 404 User not found
    @apiError 401 Token missing || missing admin permission
    """
    return delete_user(current_user, id)


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
    except Exception as exc:
        raise exc


@bp.route('/users/list/<product_id>', methods=['DELETE'])
@token_required
def purge_product(current_user, product_id):
    """
    @api {delete} /users/list/:product_id
    Remove Product
    @apiName remove_product
    @apiGroup User

    @apiHeader {String} x-access Authorization Token

    @apiParam {Number} product_id Product ID

    @apiExample Request
        curl --location --request DELETE 'http://localhost:5000/api/users/list/1bf0f365-fbdd-4e21-9786-da459d78dd1f' \
            --header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNlcnJvbmVzIiwiZXhwIjoxNjA4OTQ3NDQyfQ.QaVLQmEFiieYRiHTvbnBipBj5r1St2WvAudG_HwqVSU'

    @apiSuccess {json} Product removed
        HTTP/1.1 202

    @apiSuccessExample {json} Product removed
        {
            "message": "successfully deleted"
        }

    @apiError 404 User not found
    @apiError 401 Token missing || missing admin permission
    """
    try:
        print('started here')
        product = Product.query.filter(
            Product.user.has(id=current_user.id),
            product_id == product_id).first()
        print('product: ', product)
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

    except Exception:
        return jsonify(
            {
                'message': 'An error as ocurred'
            }
        ), HTTPStatus.INTERNAL_SERVER_ERROR
