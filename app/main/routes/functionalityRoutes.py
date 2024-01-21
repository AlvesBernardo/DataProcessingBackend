from app.extensions import db
from app.extensions import call_stored_procedure_get , call_stored_procedure_post
from flask import Flask, Blueprint,  jsonify
from itsdangerous import URLSafeTimedSerializer
from app.models.classification_model import Classification
from app.models.genre_model import Genre
from app.models.movie_model import Movie
from app.models.view_model import View
from sqlalchemy.orm import scoped_session
import datetime
from datetime import timedelta,time
from dateutil.parser import parse
from app.services.auth_guard import auth_guard,check_jwt_token
functionality_routes = Blueprint('functionality_routes', __name__)
s = URLSafeTimedSerializer('secret')

play_time_counter = {}
@functionality_routes.route('/play_movie/<int:profile_id>/<int:movie_id>')
@auth_guard('user')
def play_movie(profile_id,movie_id):
    profile_id = str(profile_id)
    movie_id = str(movie_id)
    if profile_id in play_time_counter:
        return jsonify({"message" : "movie cannot be played at the moment"})
    else :
        play_time_counter[profile_id] = {"movie" : movie_id , "start_counter" : datetime.datetime.now()}
        return jsonify({"message" : "movie played successfully"})

@functionality_routes.route('/pause_movie/<int:profile_id>/<int:movie_id>/', methods = ['GET','POST'])
@auth_guard()
def pause_movie(profile_id,movie_id):
    profile_id = str(profile_id)
    movie_id = str(movie_id)
    if profile_id in play_time_counter:
        #calculates how much you played of the movie
        time_played = datetime.datetime.now() - play_time_counter[profile_id]["start_counter"]
        view = View.query.filter_by(fiMovie = movie_id, fiProfile = profile_id).first()
        play_time_counter.pop(profile_id)
        if view == None :
            hours, remainder = divmod(time_played.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_object = time(int(hours), int(minutes), int(seconds))
            new_profile_data = (4, movie_id,profile_id, time_object)
            end_message = call_stored_procedure_post("""InsertView
                                                                                                @SubtitleID = ?,
                                                                                                @MovieID = ? ,
                                                                                                @ProfileID = ? ,
                                                                                                @MovieTime = ? 
                                                                                                """, new_profile_data)

            if end_message == []:
                return jsonify({'message': 'new view added'})
            else:
                return jsonify({'message': 'view could not be added', 'error_message': end_message})
        else :
            hours, remainder = divmod(time_played.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_object = time(int(hours), int(minutes), int(seconds))
            # update the view.dtMovieTime
            db.session.commit()

            return jsonify({'message ' : f"you have watched {view.dtMovieTime} of the movie"})

    else :
        return jsonify({'message' : 'movie cannot be stopped at the moment'})





@functionality_routes.route('/get_times_played/<int:movieId>')
@auth_guard('user')
def getHowManyTimesMoviePlayed(movieId = None):
    pass

