from app.services.emailSender import send_email
from app.extensions import db
from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.account_model import Account
from itsdangerous import URLSafeTimedSerializer
from app.services.jwt_handler import generate_jwt_token
security = Blueprint('security', __name__)
s = URLSafeTimedSerializer('secret')
@security.route('/login', methods=['POST'])
def login():
    """
    Authenticate user credentials and allow login.

    :return: Response message with appropriate status code
    """
    data = request.get_json()
    if not data or not 'dtEmail' in data or not 'dtPassword' in data:
        return jsonify({'message': 'Bad Request'}), 400

    user = Account.query.filter_by(dtEmail=data['dtEmail']).first()
    print(user.dtEmail)

    if user and user.dtPassword == data['dtPassword']:
        token = generate_jwt_token(payload= data,lifetime=3000)
        return jsonify({'message': 'Logged in successfully','token' : token}), 200
    else:
        return jsonify({'message': 'Incorrect email or password'}), 401

@security.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    :return: A JSON response with a success or error message.
    :rtype: json

    :raises: None
    """
    data = request.get_json()

    if not data or not 'dtEmail' in data or not 'dtPassword' in data:
        return jsonify({'message': 'Bad Request'}), 400

    user = Account.query.filter_by(dtEmail=data['dtEmail']).first()

    if user:
        return jsonify({"message": "User Already Exists. Please Login"}), 409
    else:
        new_user = Account(
            dtEmail=data['dtEmail'],
            dtPassword=generate_password_hash(data['dtPassword'])
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registered successfully'}), 201

@security.route('/sendEmail')
def sendingEmail(recieverEmail, subject, body):
    """
    Sends an email to the specified receiver email address.

    :param recieverEmail: The email address of the receiver.
    :param subject: The subject of the email.
    :param body: The body content of the email.
    :return: None
    """
    send_email(recieverEmail, subject, body)
@security.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Sends a password reset email to the user.

    :return: A JSON response indicating the status of the password reset request.
    """
    email = request.form.get('dtEmail')
    if not email:
        return jsonify({'message': 'Email is required'}), 400

    user = Account.query.filter_by(dtEmail=email).first()
    if not user:
        return jsonify({'message': 'User does not exist'}), 404

    token = s.dumps(email, salt='email-confirm')

    link = url_for('reset_password', token=token, _external=True, _scheme='https')
    subject = 'Password Reset Requested'
    body = 'Please follow this link to reset your password: {}'.format(link)

    send_email(email, subject, body)

    return jsonify({'message': 'An email has been sent with instructions to reset your password.'}), 200
@security.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    """
    Reset Password

    Resets the password for a user.

    :param token: The token used for password reset.
    :return: A JSON response with a message indicating the result of the password reset.
    """
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        return jsonify({'message': 'The confirmation link is invalid or has expired.'}), 400

    user = Account.query.filter_by(dtEmail=email).first()

    if not user:
        return jsonify({'message': 'User does not exist'}), 404

    new_password = request.form.get('dtPassword')
    if not new_password:
        return jsonify({'message': 'Password is required'}), 400

    user.dtPassword = generate_password_hash(new_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Your password has been reset!'}), 200



