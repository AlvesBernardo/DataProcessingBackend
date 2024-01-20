from app.extensions import db
from app.extensions import call_stored_procedure_get , call_stored_procedure_post
from flask import Flask, Blueprint,  jsonify
from itsdangerous import URLSafeTimedSerializer
from app.models.classification_model import Classification
from app.models.genre_model import Genre
from app.models.movie_model import Movie
from app.models.view_model import View
import datetime
from dateutil.parser import parse
from app.services.auth_guard import auth_guard,check_jwt_token
functionality_routes = Blueprint('functionality_routes', __name__)
s = URLSafeTimedSerializer('secret')

@functionality_routes.route('/play_movie/<int:movie_id>/')
@auth_guard('user')
def play_movie(movie_id):
    view = db.session.query(View).join(Movie, id == View.idView).filter(Movie.idMovie == id).first()
    try:
        decoded_token = check_jwt_token()
    except Exception as e:
        return jsonify({'message': e})

    # view = session.query(ViewModel).join(MovieModel).filter(MovieModel.c.dtTitle == movie_title).first()

    # if movie_title not in play_count:
    #     play_count[movie_title] = 1
    # else:
    #     play_count[movie_title] += 1


@functionality_routes.route('/stop_movie/<int:movie_id')
@functionality_routes.route('/get_times_played/<int:movieId>')
@auth_guard('user')
def getHowManyTimesMoviePlayed(movieId):
    pass

