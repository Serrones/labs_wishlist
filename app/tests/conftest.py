import os
import sys

import pytest

from app import create_app, db

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def app():
    app = create_app()
    app = create_app()
    app.config['TESTING'] = True
    db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
    app.app_context().push()
    client = app.test_client()  # noqa
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()


@pytest.fixture
def user_payload():
    return {
        'username': 'fake_user',
        'email': 'fake@email.com',
        'is_admin': True,
        'password': 'fake-pass'
    }


@pytest.fixture
def user_payload_2():
    return {
        'username': 'fake_user_2',
        'email': 'fake_user_2@email.com',
        'is_admin': False,
        'password': 'fake-pass'
    }


@pytest.fixture
def valid_product():
    return {
        'price': 1699,
        'image': 'http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg',  # noqa
        'brand': 'bébé confort',
        'id': '1bf0f365-fbdd-4e21-9786-da459d78dd1f',
        'title': 'Cadeira para Auto Iseos Bébé Confort Earth Brown'
    }
