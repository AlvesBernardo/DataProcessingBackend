from .extensions import db
from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
from app.config.connection_configuration import engine, session
from app.main.routes.securityRoutes import security
from app.main.routes.userRoutes import user_route
from app.main.routes.movieRoutes import movie_routes
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine.url  # Use the configured database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
app.register_blueprint(user_route)
app.register_blueprint(security)
app.register_blueprint(movie_routes)
# @app.route('/email')
# def sendingEmail():  # put application's code here
#      send_email('mahdisadeghi.business@gmail.com')
if __name__ == '__main__':
    app.run(debug=True)
