from .extensions import db
from flask import Flask
from app.config.connection_configuration import engine
from app.main.routes.securityRoutes import security
from app.main.routes.userRoutes import user_route
from app.main.routes.movieRoutes import movie_routes
from app.main.routes.functionalityRoutes import functionality_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine.url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
app.register_blueprint(user_route)
app.register_blueprint(security)
app.register_blueprint(movie_routes)
app.register_blueprint(functionality_routes)

if __name__ == '__main__':
    app.run(debug=True)
