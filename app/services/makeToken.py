import sys
sys.path.append("..")  # Adjust the path based on your project structure
from services.jwt_handler import generate_jwt_token

def make_token():
    payload = {"user_id": 123, "username": "test_user"}
    token = generate_jwt_token(payload, lifetime=60)  # Lifetime in minutes
    print(f"Generated Token: {token}")  # Add this line to print the generated token

    return token

if __name__ == "__main__":
    # If executed as a script, print the generated token
    print(f"Generated Token: {make_token()}")
