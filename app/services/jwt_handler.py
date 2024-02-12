import os
from jwcrypto import jwk, jwt
from jwcrypto.common import json_encode
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sys

sys.path.append("..")
load_dotenv()

def generate_jwt_token(payload,lifetime=60):
    token = generate_token(payload, lifetime, "HS256")
    return token

def generate_refresh_token(payload,lifetime=1440): # is valid for 24 hours or 1440 minutes
    token = generate_token(payload, lifetime, "HS512")
    return token

def generate_token(payload, lifetime, algorithm):
    if lifetime:
        payload["exp"] = (datetime.now() + timedelta(minutes=lifetime)).isoformat()

    secret_key = os.environ.get('SECRET_KEY')
    key = jwk.JWK(kty='oct', k=secret_key)
    token = jwt.JWT(header={"alg": algorithm}, claims=payload)
    token.make_signed_token(key)
    return token.serialize()

def decode_jwt_token(token):
    key = jwk.JWK(kty='oct', k=os.environ.get('SECRET_KEY'))
    verified_jwt = jwt.JWT(key=key, jwt=token)
    return json_encode(verified_jwt.claims)