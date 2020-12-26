from app.api import bp
from app.authentication import auth, token_required
from app.views import (create_user, delete_user, get_product, get_user,
                       get_users, remove_product, update_user)


@bp.route('/auth', methods=['GET'])
def authenticate():
    """
    @api {get} /auth
    Return Token
    @apiName authentication
    @apiGroup Auth

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
    """  # noqa
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
    """  # noqa
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
    """  # noqa
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
    """  # noqa
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
    """  # noqa
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
    """  # noqa
    return delete_user(current_user, id)


@bp.route('/users/list/<product_id>', methods=['GET'])
@token_required
def fetch_product(current_user, product_id):
    """
    @api {get} /users/list/:product_id
    Add Product
    @apiName get_product
    @apiGroup Product

    @apiHeader {String} x-access Authorization Token

    @apiParam {Number} product_id Product ID


    @apiExample Request
        HTTP/1.1 200 OK
        curl --location --request GET 'http://localhost:5000/api/users/list/1bf0f365-fbdd-4e21-9786-da459d78dd1f' \
            --header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJlbGEiLCJleHAiOjE2MDkwMTk2OTl9.7wRC4JB0n_0-bYAAIF8Fny4f-c33q8sf0hgvmUL8h38'

    @apiSuccess {Object} oret Product fetched
        HTTP/1.1 200 Ok
    
    @apiSuccessExample {json} Product
        HTTP/1.1 200 OK
        {
            "message": "product added in list"
        }
    @apiError 401 User not found || token missing
    @apiError 404 Product not found
    """  # noqa
    return get_product(current_user, product_id)


@bp.route('/users/list/<product_id>', methods=['DELETE'])
@token_required
def purge_product(current_user, product_id):
    """
    @api {delete} /users/list/:product_id
    Remove Product
    @apiName remove_product
    @apiGroup Product

    @apiHeader {String} x-access Authorization Token

    @apiParam {Number} product_id Product ID

    @apiExample Request
        curl --location --request DELETE 'http://localhost:5000/api/users/list/1bf0f365-fbdd-4e21-9786-da459d78dd1f' \
            --header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNlcnJvbmVzIiwiZXhwIjoxNjA4OTQ3NDQyfQ.QaVLQmEFiieYRiHTvbnBipBj5r1St2WvAudG_HwqVSU'

    @apiSuccess {json} Product removed
        HTTP/1.1 202

    @apiSuccessExample {json} Product removed
        {
            "message": "product removed from list"
        }

    @apiError 404 Product not found in User List
    @apiError 401 Token missing
    """  # noqa
    return remove_product(current_user, product_id)
