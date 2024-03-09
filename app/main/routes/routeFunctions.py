from app.services.jwt_handler import generate_jwt_token, generate_refresh_token, decode_jwt_token
from app.extensions import call_stored_procedure_post
from flask import jsonify
import datetime
from datetime import time,datetime, timedelta, timezone
from app.models.classification_model import Classification
from app.models.profile_model import Profile
from app.models.movie_model import Movie
from app.models.view_model import View
from app.models.timesPlayed_model import TimesPlayed
from app.extensions import db
def calculate_final_time(time_played:datetime):
    hours, remainder = divmod(time_played.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    time_object = time(int(hours), int(minutes), int(seconds))
    return time_object


def update_date_time(view:View,time_played:datetime):
    reference_date = datetime.date.today()
    datetime_obj = datetime.datetime.combine(reference_date, view.dtMovieTime)
    updated_datetime = datetime_obj + time_played
    view.dtMovieTime = updated_datetime.time()
    # update the view.dtMovieTime
    db.session.commit()

def check_if_account_is_blocked(user) : 
    if user.isAccountBlocked and user.dtAccountBlockedTill and user.dtAccountBlockedTill > datetime.now(timezone.utc) :
                   return True
    else :
        return False
    

def generate_new_token(user_info,user) :
    refresh_token = generate_refresh_token(payload=user_info)
    user.dtRefreshToken = refresh_token
    user.dtRefreshToken_valid_until = datetime.now(timezone.utc) + timedelta(days=1)
    token = generate_jwt_token(payload=user_info)
    return (refresh_token, token)


def handle_access_token(user_info,user,data):
    refreshToken = user.dtRefreshToken
    if refreshToken:
        try :
            decoding_value = decode_jwt_token(refreshToken)
            if decoding_value:
                token = generate_jwt_token(payload=user_info) 
        except:
            token = generate_jwt_token(payload=user_info)
    else:
        (refresh_token, token) = generate_new_token(user_info,user)
        loginValues = (data['dtEmail'], refresh_token)
        db.session.commit(loginValues)
        db.session.commit()
        call_stored_procedure_post("""InsertRefreshToken
                                                        @email = ?,
                                                        @refreshToken = ?, 
                                                        """, loginValues)
    return token
def failed_login_attempt(user) : 
    user.dtFailedLoginAttempts += 1
    if user.dtFailedLoginAttempts >= 3:
        user.isAccountBlocked = True
        user.dtAccountBlockedTill = datetime.now(timezone.utc) + timedelta(minutes=60)

    db.session.commit() 

    return jsonify({'message': 'Incorrect email or password'}), 401
def get_multiple_objects(query_list,attribute_list:list) :
    output = []
    for object in query_list :
        object_data = {}
        try :
            for attribute in attribute_list :
                object_data[attribute] = getattr(object,attribute)
            output.append(object_data)
        except Exception as e :
            return jsonify({'message': f'Error: {e}'}), 500
    return jsonify({'results':output}),200

