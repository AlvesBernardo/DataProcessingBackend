from app.config.connection_configuration import engine
from app.services.emailSender import send_email
from .extensions import db
from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
from app.controller.loginController import logIn
from app.controller.numberGenerator import randomNumberGenerator
from app.config.connection_configuration import engine, session
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from app.models.account_model import Account
from app.models.classification_model import Classification
from app.models.genre_model import Genre
from app.models.language_model import Language
from app.models.movie_model import Movie
from app.models.profile_model import Profile
from app.models.quality_model import Quality
from app.models.subscription_model import Subcription
from app.models.subtitle_model import Subtitle
from app.models.view_model import View
import datetime
import os
from main.routes.userRoutes import user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine.url  # Use the configured database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(user)

if __name__ == '__main__':
    app.run(debug=True)
