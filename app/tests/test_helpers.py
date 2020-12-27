from app.helpers import get_user_by_username
from app.views import create_user


class TestGetUserByUsername:

    def test_should_return_user(
        self,
        app,
        user_payload
    ):
        with app.test_request_context(
            '/users', json=user_payload
        ):
            create_user()

            user = get_user_by_username(user_payload['username'])

            assert user.username == user_payload['username']
            assert user.email == user_payload['email']
            assert user.is_admin == user_payload['is_admin']

    def test_should_return_none_when_user_not_found(
        self,
        app
    ):
        user = get_user_by_username('fake_username')

        assert user is None
