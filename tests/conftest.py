import os

import pytest
from datetime import datetime
from werkzeug.security import generate_password_hash
from flaskr import create_app
from flaskr import db
from flaskr import init_db
from flaskr.models import User
from flaskr.models import Post

_user1_pass = generate_password_hash("test")
_user2_pass = generate_password_hash("other")

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })

    with app.app_context():
        init_db()
        user1 = User(username="test", _password=_user1_pass)
        user2 = User(username="other", _password=_user2_pass)
        post = Post(
            title='test title',
            body='test\nbody',
            author=user1,
            created=datetime(2018, 1, 1),
        )
        db.session.add_all((user1, user2, post))
        db.session.commit()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
