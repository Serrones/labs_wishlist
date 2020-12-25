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
