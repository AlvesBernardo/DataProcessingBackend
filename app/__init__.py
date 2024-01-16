from flask import Flask
from config import Config
def create_app (config_app=Config):
    app = Flask(__name__)
    app.config.from_object(config_app)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    return app

