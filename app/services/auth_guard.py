from flask import request, jsonify
from .jwt_handler import decode_jwt_token
from datetime import datetime, timedelta


def check_jwt_token(token=None):
    if token is None:
        token = request.headers.get('Authorization', "")
        if not token:
            raise Exception('Missing access token')
        token = token.replace('Bearer ', '').strip()
    try:
        decoded_token = decode_jwt_token(token)
        return decoded_token
    except Exception as e:
        raise Exception(f'Invalid authGuard access token: {e}')


def auth_guard(role=None):
    def wrapper(route_function):
        def decorated_function(*args, **kwargs):
            try:
                user_data = check_jwt_token()
            except Exception as e:
                return jsonify({"message": f'{e}', "status": 401}), 401

            user_role = user_data.get('roles', '')
            if role and not (user_role == "user" or user_role == 'admin'):
                return jsonify({"message": 'Authorization required.', "status": 403}), 403

            return route_function(*args, **kwargs)

        decorated_function.__name__ = route_function.__name__
        return decorated_function

    return wrapper
