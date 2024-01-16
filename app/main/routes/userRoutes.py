# user_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
import sys
sys.path.append("..") # added!
from controller.loginController import logIn
#from controller.numberGenerator import randomNumberGenerator
#from models.movie_model import MovieModel
from ..config.connection_configuration import engine, session
user_routes_bp = Blueprint('user_routes', __name__)
play_count = {}
def logInUser():
    error_message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not is_valid_email(email):
            error_message = 'Invalid email format'
        elif not is_valid_password(password):
            error_message = 'Password must be minimum 8 characters and contain at least one uppercase letter, one lowercase letter, one number, and one special character'
        else:
            if login(email, password):
                return redirect(url_for('user_routes.success'))
            else:
                error_message = 'Invalid credentials'
def register():
    print("test")
    if request.method == 'POST':
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')
        #if we have time check for duplicate emails
        success, message = registerUser(name, email, password)
        try:
            if success:
                return jsonify({"message": message}), 201
            else:
                return jsonify({"message": message}), 400
        except Exception as error:
            print("Error during user registration:", error)
            return jsonify({"message": "Failed to register user"}), 500
    else:
        return jsonify({"message": "Method not allowed"}), 405


def forgotPassword():    
    error_message = None

    if request.method == 'POST':
        
        email = request.form['email']

        if not is_valid_email(email):
            error_message = 'Invalid email format'
        else:
            email_data = {'email': email}
            email_response = requests.post(f'{API_BASE_URL}/forgotPass', json=email_data)
            if email_response.status_code == 200:
                return redirect(url_for('success'))
            else:
                error_message = 'Invalid credentials'


#def getInvitationCode():
    number = randomNumberGenerator


def play_movie():
    movie_title = request.form["movie_title"]
    
    view = session.query(ViewModel).join(MovieModel).filter(MovieModel.c.dtTitle == movie_title).first()

    if movie_title not in play_count:
        play_count[movie_title] = 1
    else:
        play_count[movie_title] += 1

    
def getHowManyTimesMoviePlayed(Movie):
    movie_title = request.args.get('movie_title')

    if movie_title not in play_count:
        return jsonify("movie never played")
    else:
        return jsonify(play_count[movie_title])
    
def forgotPass():
    
    error_message = None

    if request.method == 'POST':
        
        email = request.form['email']

        if not is_valid_email(email):
            error_message = 'Invalid email format'
        else:
            email_data = {'email': email}
            email_response = requests.post(f'{API_BASE_URL}/forgotPass', json=email_data)
            if email_response.status_code == 200:
                return redirect(url_for('success'))
            else:
                error_message = 'Invalid credentials'

    return render_template('forgotPass.html', error_message=error_message)
