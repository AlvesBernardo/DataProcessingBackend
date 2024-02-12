import sys
sys.path.append("..")
from jwt_handler import generate_jwt_token, generate_refresh_token

def make_token():
    payload = {"user_id": 123, "username": "test_user"}
    access_token = generate_jwt_token(payload, lifetime=60)
    refresh_token = generate_refresh_token(payload, lifetime=2880)

    return access_token, refresh_token

if __name__ == "__main__":
    print(f"Generated Token: {make_token()}")
