import os
from jwcrypto import jwk, jwt
from datetime import datetime, timezone
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sys
import json
from jwcrypto import jwt, jwk

sys.path.append("..")
load_dotenv()


def generate_jwt_token(payload, lifetime=60):
    token = generate_token(payload, lifetime, "HS256")
    return token


def generate_refresh_token(payload, lifetime=2880):
    token = generate_token(payload, lifetime, "HS256")
    return token


def generate_token(payload, lifetime, algorithm):
    if lifetime:
        # Set 'exp' to a Unix timestamp (integer)
        payload["exp"] = int((datetime.now() + timedelta(minutes=lifetime)).timestamp())
    
    secret_key = os.environ.get('SECRET_KEY')
    key = jwk.JWK(kty='oct', k=secret_key)
    token = jwt.JWT(header={"alg": algorithm}, claims=payload)
    token.make_signed_token(key)
    return token.serialize()


def decode_jwt_token(token):
    try:
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            raise ValueError("SECRET_KEY is not set")

        key = jwk.JWK(kty='oct', k=secret_key)
        jwt_token = jwt.JWT(key=key, jwt=token)
        jwt_token.deserialize(token, key=key)

        claims = jwt_token.claims

        # Check if claims is a string and convert it to a dictionary
        if isinstance(claims, str):
            claims = json.loads(claims)

        # Assuming exp claim is a Unix timestamp
        exp_time = datetime.fromtimestamp(int(claims['exp']), timezone.utc)
        if exp_time > datetime.now(timezone.utc):
            return claims
        else:
            return False
    except Exception as e:
        raise Exception(f'Invalid access token: {e}')
