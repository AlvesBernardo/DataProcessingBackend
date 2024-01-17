from flask import Flask
from app.config.connection_configuration import engine
from app.services.emailSender import send_email
from app.extensions import db
from app.models.view_model import View
from app.main.routes.userRoutes import adminRegister, test_connection, getHowManyTimesMoviePlayed
#from .main.routes.userRoutes import register
from app import create_app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine.url  # Use the configured database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app = create_app()

app.register_blueprint(adminRegister)
app.register_blueprint(test_connection)
# app.register_blueprint(getHowManyTimesMoviePlayed)
# @app.route('/email')
# def sendingEmail():  # put application's code here
#      send_email('mahdisadeghi.business@gmail.com')




if __name__ == '__main__':
    app.run()
