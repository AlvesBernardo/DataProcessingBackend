from flask import Flask
from config import Config
from app.extensions import db
def create_app (config_app=Config):
    app = Flask(__name__)
    app.config.from_object(config_app)
    db.init_app(app)
    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    return app

