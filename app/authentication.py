from datetime import datetime, timedelta
from functools import wraps
from http import HTTPStatus

import jwt
from flask import jsonify, request

from app.helpers import get_user_by_username
from config import Config

SECRET_KEY = Config.SECRET_KEY

def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify(
            {
                'message': 'coud not verify',
                'WWW-Authentication': 'Basic-auth="login required"'
            }
        ), HTTPStatus.UNAUTHORIZED

    user = get_user_by_username(auth.username)
    if not user:
        return jsonify(
            {
                'message': 'user not found'
            }
        ), HTTPStatus.UNAUTHORIZED

    if user and user.check_password(auth.password):
        token = jwt.encode(
            {
                'username': user.username,
                'exp': datetime.now() + timedelta(hours=12)
            },
            SECRET_KEY
        )
        return jsonify(
            {
                'message': 'Validated sucessfully',
                'token': token.decode('UTF-8'),
                'exp': datetime.now() + timedelta(hours=12)
            }
        )
    return jsonify(
        {
            'message': 'coud not verify',
            'WWW-Authentication': 'Basic-auth="login required"'
        }
    ), HTTPStatus.UNAUTHORIZED


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify(
                {
                    'message': 'token is missing'
                }
            ), HTTPStatus.UNAUTHORIZED
        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = get_user_by_username(username=data['username'])
        except Exception:
            return jsonify(
                {
                    'message': 'token is invalid or expired'
                }
            ), HTTPStatus.UNAUTHORIZED
        return f(current_user, *args, **kwargs)
    return decorated
