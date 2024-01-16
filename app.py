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
# from controller.register import registerUser
from controller.checkSubtitle import get_subtitle
import xml.etree.ElementTree as ET





app.config['SQLALCHEMY_DATABASE_URI'] = str(engine.url)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = engine
db = SQLAlchemy(app)
logger = logging.getLogger(__name__)
#routes 
from routes.userRoutes import logInUser, register, forgotPassword, play_movie, getHowManyTimesMoviePlayed, getHowManyTimesMoviePlayed 


def dict_to_xml(d):
    root = ET.Element('response')
    for key, value in d.items():
        child = ET.Element(key)
        child.text = str(value)
        root.append(child)
    return ET.tostring(root, encoding='utf-8', method='xml')

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

# @app.route('/register', methods=['POST', 'OPTIONS'])
# def register():
#     if request.method == 'OPTIONS':
#         # Handling preflight request
#         response = make_response()
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Allow-Methods', 'POST')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         return response

#     # Handling actual POST request
    
#     email = request.json.get('email')
#     password = request.json.get('password')
#     #if we have time, check for duplicate emails
#     success, message = registerUser(email, password)

#     try:
#         if success:
#             response = jsonify({"message": message})
#             response.headers.add('Access-Control-Allow-Origin', '*')
#             return response, 201
#         else:
#             response = jsonify({"message": message})
#             response.headers.add('Access-Control-Allow-Origin', '*')
#             return response, 400
#     except Exception as error:
#         print("Error during user registration:", error)
#         response = jsonify({"message": "Failed to register user"})
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         return response, 500



# app.add_url_rule("/login", view_func=logInUser, methods=["POST"])
# #app.add_url_rule("/register", view_func=register, methods=["POST"])
# app.add_url_rule("/forgotPassword", view_func=forgotPassword, methods=["POST"])
# #app.add_url_rule("/getInvitationCode",view_func=getInvitationCode, methods=["POST"])
# app.add_url_rule("/forgotPass", view_func=forgotPassword, methods=["POST"])
# app.add_url_rule("/profile/playMovie",view_func=play_movie, methods=["POST"])
# app.add_url_rule("/profile/getHowManyTimesMoviePlayed", view_func=getHowManyTimesMoviePlayed, methods=["POST"])


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



@app.route('/movie/turnSubtitleOn', methods=['POST'])
def turn_subtitle_on():
    movie_id = request.json.get('movie')
    language = request.json.get('language')
    
    subtitle = get_subtitle(language)

    if subtitle:
        response_data = {"message": f"Subtile found"}
    else:
        response_data = {"message": "Subtitle not found"}

    return dict_to_xml(response_data),200, {'Content-Type': 'application/xml'}

# @app.route('/movie/turnSubtitleOff', methods=['POST'])
# def turn_subtitle_off():
#     movie_id = request.json.get('movie')

#     # Set the subtitle for the given movie to None or an empty string
#     set_subtitle(movie_id, None)  # or set_subtitle(movie_id, '')

#     response_data = {"message": "Subtile turned off"}
#     return xmlify(response_data),200, {"Content-Type": "application/xml"}


if __name__ == '__main__':
    app.run(debug=True, port=8080)
