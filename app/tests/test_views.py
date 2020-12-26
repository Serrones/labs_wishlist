from http import HTTPStatus

from app.models import User
from app.views import (create_user, delete_user, get_user, get_users,
                       update_user)


class TestCreateUser:

    def test_create_user_should_return_created(
        self,
        user_payload,
        app
    ):
        with app.test_request_context(
            '/users', json=user_payload
        ):
            response = create_user()

            message = response[0].json['message']
            username = response[0].json['data']['username']

            assert response[1] == HTTPStatus.CREATED
            assert message == 'User created'
            assert username == user_payload['username']

    def test_create_user_should_return_bad_request_when_missing_field(
        self,
        user_payload,
        app
    ):
        del user_payload['username']
        with app.test_request_context(
            '/users', json=user_payload
        ):
            response = create_user()

            message = response[0].json['Error']

            assert response[1] == HTTPStatus.BAD_REQUEST
            assert message == 'Missing field username'

    def test_create_user_should_return_forbidden_when_user_already_created(
        self,
        user_payload,
        app
    ):

        with app.test_request_context(
            '/users', json=user_payload
        ):
            create_user()

            response = create_user()

            message = response[0].json['Error']

            assert response[1] == HTTPStatus.FORBIDDEN
            assert message == 'Already exists user with this username'


class TestGetUsers:

    def test_get_users_should_return_success(
        self,
        app,
        user_payload
    ):
        with app.test_request_context(
            '/users', json=user_payload
        ):
            create_user()

        with app.test_request_context('/users'):
            users = get_users()

            message = users[0].json['message']

            assert users[1] == HTTPStatus.OK
            assert message == 'success'

    def test_get_users_should_return_success_even_not_users(
        self,
        app
    ):

        with app.test_request_context('/users'):
            users = get_users()

            message = users[0].json['message']

            assert users[1] == HTTPStatus.OK
            assert message == 'no users'


class TestGetUser:

    def test_get_user_should_return_success(
        self,
        app,
        user_payload
    ):

        with app.test_request_context(
            '/users', json=user_payload
        ):
            create_user()

        with app.test_request_context('/users?id=id'):
            user = get_user(1)

            message = user[0].json['message']
            username = user[0].json['data']['username']

            assert user[1] == HTTPStatus.OK
            assert message == 'successfully fetched'
            assert username == user_payload['username']

    def test_get_user_should_return_not_found(
        self,
        app
    ):

        with app.test_request_context('/users?id=id'):
            user = get_user(1)

            message = user[0].json['message']

            assert user[1] == HTTPStatus.NOT_FOUND
            assert message == 'user not found'


class TestUpdateUser:

    def test_update_user_should_return_created(
        self,
        app,
        user_payload
    ):

        with app.test_request_context(
            '/users', json=user_payload
        ):
            create_user()

        user_payload['email'] = 'another@email.com'
        with app.test_request_context(
            '/users?id=id', json=user_payload
        ):

            user = User.query.get(1)

            assert user.email == 'fake@email.com'

            updated_user = update_user(user, 1)

            message = updated_user[0].json['message']
            email = updated_user[0].json['data']['email']

            assert updated_user[1] == HTTPStatus.CREATED
            assert message == 'successfully updated'
            assert email == 'another@email.com'

    def test_update_user_should_return_unauthorized(
        self,
        app,
        user_payload_2
    ):
        with app.test_request_context(
            '/users', json=user_payload_2
        ):
            create_user()

        with app.test_request_context(
            '/users?id=id', json=user_payload_2
        ):

            user = User.query.get(1)

            updated_user = update_user(user, 1)

            message = updated_user[0].json['message']

            assert updated_user[1] == HTTPStatus.UNAUTHORIZED
            assert message == 'you dont have permission'

    def test_update_user_should_return_not_found(
        self,
        app,
        user_payload
    ):
        with app.test_request_context(
            '/users', json=user_payload
        ):
            create_user()

        with app.test_request_context(
            '/users?id=id', json=user_payload
        ):

            user = User.query.get(1)

            updated_user = update_user(user, 100)

            message = updated_user[0].json['message']

            assert updated_user[1] == HTTPStatus.NOT_FOUND
            assert message == 'user doesnt exists'

    def test_update_user_should_return_bad_request(
        self,
        app,
        user_payload
    ):
        with app.test_request_context(
            '/users', json=user_payload
        ):
            create_user()

        user_payload['foo'] = 'bar'
        with app.test_request_context(
            '/users?id=id', json=user_payload
        ):

            user = User.query.get(1)

            updated_user = update_user(user, 1)

            message = updated_user[0].json['Error']

            assert updated_user[1] == HTTPStatus.BAD_REQUEST
            assert message == 'Invalid field'


class TestDeleteUser:

    def test_delete_user_should_return_accepted(
        self,
        app,
        user_payload,
        user_payload_2
    ):

        with app.test_request_context(
            '/users', json=user_payload
        ):
            create_user()

        with app.test_request_context(
            '/users', json=user_payload_2
        ):
            create_user()

        with app.test_request_context('/users?id=id'):

            user = User.query.get(1)

            deleted_user = delete_user(user, 2)

            message = deleted_user[0].json['message']

            assert deleted_user[1] == HTTPStatus.ACCEPTED
            assert message == 'successfully deleted'

    def test_delete_user_should_return_unauthorized(
        self,
        app,
        user_payload_2
    ):
        with app.test_request_context(
            '/users', json=user_payload_2
        ):
            create_user()

        with app.test_request_context('/users?id=id'):

            user = User.query.get(1)

            deleted_user = delete_user(user, 1)

            message = deleted_user[0].json['message']

            assert deleted_user[1] == HTTPStatus.UNAUTHORIZED
            assert message == 'you dont have permission'

    def test_delete_user_should_return_not_found(
        self,
        app,
        user_payload
    ):
        with app.test_request_context(
                '/users', json=user_payload
        ):
            create_user()

        with app.test_request_context('/users?id=id'):

            user = User.query.get(1)

            deleted_user = delete_user(user, 100)

            message = deleted_user[0].json['message']

            assert deleted_user[1] == HTTPStatus.NOT_FOUND
            assert message == 'user not found'
