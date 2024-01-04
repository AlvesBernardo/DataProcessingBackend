from flask import request
from services.jwt_handler import decote_jwt_token
from flask import jsonify

def check_jwt_token():
    # Gets token from request header and tries to get it's payload
    token = request.headers.get('Authorization')
    if not token:
        raise Exception('Missing access token')

    jwt_parts = token.split('Bearer ')
    if len(jwt_parts) < 2:
        raise Exception('Invalid access token format')

    jwt = jwt_parts[1]
    try:
        return decote_jwt_token(jwt)
    except Exception as e:
        raise Exception(f'Invalid access token: {e}')

def auth_guard(role=None):
    def wrapper(route_function):
        def decorated_function(*args, **kwargs):
            #Authentication gate
            try:
                user_data = check_jwt_token()
            except Exception as e:
                 return jsonify({"message": f'{e}', "status": 401}), 401
            return route_function(*args, **kwargs)
            
        decorated_function.__name__= route_function.__name__
        return decorated_function
    return wrapper        
