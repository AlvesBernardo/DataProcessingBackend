# app.py
from flask import Flask, render_template,request, jsonify, make_response
import sys
sys.path.append("..") # added!
from services.auth_guard import *
from services.jwt_handler import generate_jwt_token
app = Flask(__name__)
from flask import jsonify
import requests
from services.jwt_handler import decode_jwt_token
from services.auth_guard import check_jwt_token
from services.makeToken import make_token
from config.connection_configuration import session, engine
from flask_sqlalchemy import SQLAlchemy
import logging  # Add this import statement
from controller.register import registerUser
app.config['SQLALCHEMY_DATABASE_URI'] = str(engine.url)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = engine
db = SQLAlchemy(app)
logger = logging.getLogger(__name__)
#routes 
from routes.userRoutes import logInUser, register, forgotPassword, play_movie, getHowManyTimesMoviePlayed, getHowManyTimesMoviePlayed 

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

@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        # Handling preflight request
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    # Handling actual POST request
    print("Test")
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    
    #if we have time, check for duplicate emails
    print(name)
    success, message = registerUser(name, email, password)

    try:
        if success:
            response = jsonify({"message": message})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 201
        else:
            response = jsonify({"message": message})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
    except Exception as error:
        print("Error during user registration:", error)
        response = jsonify({"message": "Failed to register user"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500



app.add_url_rule("/login", view_func=logInUser, methods=["POST"])
#app.add_url_rule("/register", view_func=register, methods=["POST"])
app.add_url_rule("/forgotPassword", view_func=forgotPassword, methods=["POST"])
#app.add_url_rule("/getInvitationCode",view_func=getInvitationCode, methods=["POST"])
app.add_url_rule("/forgotPass", view_func=forgotPassword, methods=["POST"])
app.add_url_rule("/profile/playMovie",view_func=play_movie, methods=["POST"])
app.add_url_rule("/profile/getHowManyTimesMoviePlayed", view_func=getHowManyTimesMoviePlayed, methods=["POST"])


# Dummy protected route
@app.route('/protected_route', methods=['GET'])
def protected_route():
    
    token = make_token()
    auth_guard
    try:
        # Call check_jwt_token as a standalone function with the generated token
        user_data = check_jwt_token(token)

        # Now you have access to the decoded token information
        user_id = user_data.get('user_id', None)

        return jsonify({"message": "Token is valid!", "user_id": user_id})
    
    except Exception as e:
        return jsonify({"message": f'Token validation failed: {e}', "status": 401}), 401
if __name__ == '__main__':
    app.run(debug=True, port=8080)
