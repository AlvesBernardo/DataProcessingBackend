# app.py
from flask import Flask
import sys
sys.path.append("..") # added!
from src.instances import quality_instances
from services.auth_guard import check_jwt_token
from services.jwt_handler import generate_jwt_token
app = Flask(__name__)
from flask import jsonify
import requests
from services.jwt_handler import decode_jwt_token
from services.auth_guard import check_jwt_token
from services.makeToken import make_token

@app.route('/')
def index():
    return render_template('index.html', subscriptions=quality_instances)

@app.route('/select_subscription', methods=['POST'])
#@auth_guard()
def select_subscription():
    selected_subscription_index = int(request.form['subscription'])

    # onl allow selection of subscriptions from a list
    selected_subscription = quality_instances[selected_subscription_index]
    current_user.subscription = selected_subscription


    return f"Subscription {selected_subscription.get_description()} selected for the user!"

@app.route('/get_subscription', methods=['GET'])
def get_subscription(subscription):
    if current_user.subscription:
        subscription_info = {
            'description': current_user.subscription.get_description(),
            'price': current_user.subscription.get_price()
        }
        return f"User's Subscription: {subscription_info}"
    else:
        return "User has not selected a subscription yet."

#dummy generator function


# Dummy protected route
@app.route('/protected_route', methods=['GET'])
def protected_route():
    token = make_token()

    try:
        # Call check_jwt_token as a standalone function with the generated token
        user_data = check_jwt_token(token)

        # Now you have access to the decoded token information
        user_id = user_data.get('user_id', None)

        return jsonify({"message": "Token is valid!", "user_id": user_id})
    
    except Exception as e:
        return jsonify({"message": f'Token validation failed: {e}', "status": 401}), 401
if __name__ == '__main__':
    app.run(debug=True)
