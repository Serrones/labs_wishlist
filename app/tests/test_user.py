import json

import pytest


class TestUsers:

    def test_should_create_user(self, app):
        new_user = {
            'username': 'fake_user',
            'email': 'fake@email.com',
            'is_admin': True,
            'password': 'fake-pass'
        }
        with app.test_client() as test_client:
            response = test_client.post(
                'api/users',
                data=json.dumps(new_user),
                content_type='application/json'
            )
            assert response.status_code == 201

    def test_raise_exception_when_create_user(self, app):
        with app.test_client() as test_client:
            with pytest.raises(Exception):
                test_client.post(
                    'api/users',
                    data=json.dumps({}),
                    content_type='application/json'
                )
