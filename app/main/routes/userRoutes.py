from app.services.emailSender import send_email
from app.extensions import db
from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
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
user = Blueprint('user', __name__)
s = URLSafeTimedSerializer('secret')
play_count = {}
@user.route('/login', methods=['POST'])
def login():
    """
    Authenticate user credentials and allow login.

    :return: Response message with appropriate status code
    """
    data = request.get_json()

    if not data or not 'dtEmail' in data or not 'dtPassword' in data:
        return jsonify({'message': 'Bad Request'}), 400

    user = Account.query.filter_by(dtEmail=data['dtEmail']).first()

    if user and check_password_hash(user.dtPassword, data['dtPassword']):
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Incorrect email or password'}), 401


@user.route('/register', methods=['POST'])
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
@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not 'dtEmail' in data or not 'dtPassword' in data:
        return jsonify({'message': 'Bad Request'}), 400

    user = Account.query.filter_by(dtEmail=data['dtEmail']).first()

    if user and check_password_hash(user.dtPassword, data['dtPassword']):
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Incorrect email or password'}), 401


@user.route('/register', methods=['POST'])
def register():
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


@user.route('/sendEmail')
def sendingEmail(recieverEmail, subject, body):
    send_email(recieverEmail, subject, body)


@user.route('/forgot-password', methods=['POST'])
def forgot_password():
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


@user.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
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


@user.route('/users', methods=['GET', 'POST'])
@user.route('/users/<id>', methods=['GET', 'POST', 'DELETE'])
def manage_users(id=None):
    if request.method == 'GET':
        if id:
            user = Account.query.get(id)
            if not user:
                return jsonify({'message': 'No user found!'}), 404

            user_data = {
                'idAccount': user.idAccount,
                'dtEmail': user.dtEmail,
                'isAccountBlocked': user.isAccountBlocked,
                'dtIsAdmin': user.dtIsAdmin,
                'fiSubscription': user.fiSubscription,
                'fiLanguage': user.fiLanguage
            }

            return jsonify(user_data)

        else:
            users = Account.query.all()
            output = []

            for user in users:
                user_data = {
                    'idAccount': user.idAccount,
                    'dtEmail': user.dtEmail,
                    'isAccountBlocked': user.isAccountBlocked,
                    'dtIsAdmin': user.dtIsAdmin,
                    'fiSubscription': user.fiSubscription,
                    'fiLanguage': user.fiLanguage
                }
                output.append(user_data)

            return jsonify({'users': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_user = Account(
            dtEmail=data['dtEmail'],
            dtPassword=generate_password_hash(data['dtPassword']),
            isAccountBlocked=data.get('isAccountBlocked', False),
            dtIsAdmin=data.get('dtIsAdmin', False),
            fiSubscription=data.get('fiSubscription'),
            fiLanguage=data.get('fiLanguage')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'new user added'})

    elif request.method == 'DELETE':
        user = Account.query.get(id)
        if not user:
            return jsonify({'message': 'No user found!'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'user has been deleted'})


@user.route('/subscriptions', methods=['GET', 'POST'])
@user.route('/subscriptions/<id>', methods=['GET', 'POST', 'DELETE'])
def manage_subscriptions(id=None):
    if request.method == 'GET':
        if id:
            subscription = Subcription.query.get(id)
            if not subscription:
                return jsonify({'message': 'No subscription found!'}), 404

            subscription_data = {
                'idSubscription': subscription.idSubscription
                # Add here all the other properties you want to send
            }

            return jsonify(subscription_data)

        else:  # If id is not provided, return all subscriptions
            subscriptions = Subcription.query.all()
            output = []

            for subscription in subscriptions:
                subscription_data = {
                    'idSubscription': subscription.idSubscription
                    # Add here all the other properties you want to send
                }
                output.append(subscription_data)

            return jsonify({'subscriptions': output})

    elif request.method == 'POST':
        data = request.get_json()
        # Here you'd typically validate the data format and parameters
        new_subscription = Subcription(**data)

        db.session.add(new_subscription)
        db.session.commit()

        return jsonify({'message':'new subscription added'})

    elif request.method == 'DELETE':
        subscription = Subcription.query.get(id)
        if not subscription:
            return jsonify({'message': 'No subscription found!'}), 404

        db.session.delete(subscription)
        db.session.commit()

        return jsonify({'message':'subscription has been deleted'})

def play_movie():
    movie_title = request.form["movie_title"]
    
    view = session.query(View).join(Movie).filter(Movie.c.dtTitle == movie_title).first()

@user.route('/languages', methods=['GET', 'POST'])
@user.route('/languages/<id>', methods=['GET', 'POST', 'DELETE'])
def manage_languages(id=None):
    if request.method == 'GET':
        if id:
            language = Language.query.get(id)
            if not language:
                return jsonify({'message': 'No language found!'}), 404

            language_data = {
                'idLanguage': language.idLanguage,
                'dtDescription': language.dtDescription
            }

            return jsonify(language_data)

        else:
            languages = Language.query.all()
            output = []

            for language in languages:
                language_data = {
                    'idLanguage': language.idLanguage,
                    'dtDescription': language.dtDescription
                }
                output.append(language_data)

            return jsonify({'languages': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_language = Language(**data)

        db.session.add(new_language)
        db.session.commit()

        return jsonify({'message': 'new language added'})

    elif request.method == 'DELETE':
        language = Language.query.get(id)
        if not language:
            return jsonify({'message': 'No language found!'}), 404

        db.session.delete(language)
        db.session.commit()

        return jsonify({'message': 'language has been deleted'})



def getHowManyTimesMoviePlayed(Movie):
    movie_title = request.args.get('movie_title')
@user.route('/classifications', methods=['GET', 'POST'])
@user.route('/classifications/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_classifications(id=None):
    if request.method == 'GET':
        if id:
            classification = Classification.query.get(id)
            if not classification:
                return jsonify({'message': 'No classification found!'}), 404

            classification_data = {
                'idClassification': classification.idClassification,
                'dtDescription': classification.dtDescription
            }

            return jsonify(classification_data)

        else:
            classifications = Classification.query.all()
            output = []

            for classification in classifications:
                classification_data = {
                    'idClassification': classification.idClassification,
                    'dtDescription': classification.dtDescription
                }
                output.append(classification_data)

            return jsonify({'classifications': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_classification = Classification(**data)

        db.session.add(new_classification)
        db.session.commit()

        return jsonify({'message':'new classification added'})

    elif request.method == 'PUT':
        data = request.get_json()
        classification = Classification.query.get(id)

        if not classification:
            return jsonify({'message': 'No classification found!'}), 404

        classification.dtDescription = data.get('dtDescription', classification.dtDescription)
        db.session.commit()

        return jsonify({'message':'classification updated'})

    elif request.method == 'DELETE':
        classification = Classification.query.get(id)
        if not classification:
            return jsonify({'message': 'No classification found!'}), 404

        db.session.delete(classification)
        db.session.commit()

        return jsonify({'message':'classification has been deleted'})


@user.route('/genres', methods=['GET', 'POST'])
@user.route('/genres/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_genres(id=None):
    if request.method == 'GET':
        if id:
            genre = Genre.query.get(id)
            if not genre:
                return jsonify({'message': 'No genre found!'}), 404

            genre_data = {
                'idGenre': genre.idGenre,
                'dtDescription': genre.dtDescription
            }

            return jsonify(genre_data)

        else:
            genres = Genre.query.all()
            output = []

            for genre in genres:
                genre_data = {
                    'idGenre': genre.idGenre,
                    'dtDescription': genre.dtDescription
                }
                output.append(genre_data)

            return jsonify({'genres': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_genre = Genre(**data)

        db.session.add(new_genre)
        db.session.commit()

        return jsonify({'message':'new genre added'})

    elif request.method == 'PUT':
        data = request.get_json()
        genre = Genre.query.get(id)

        if not genre:
            return jsonify({'message': 'No genre found!'}), 404

        genre.dtDescription = data.get('dtDescription', genre.dtDescription)
        db.session.commit()

        return jsonify({'message':'genre updated'})

    elif request.method == 'DELETE':
        genre = Genre.query.get(id)
        if not genre:
            return jsonify({'message': 'No genre found!'}), 404

        db.session.delete(genre)
        db.session.commit()

        return jsonify({'message':'genre has been deleted'})


@user.route('/movies', methods=['GET', 'POST'])
@user.route('/movies/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_movies(id=None):
    if request.method == 'GET':
        if id:
            movie = Movie.query.get(id)
            if not movie:
                return jsonify({'message': 'No movie found!'}), 404
            movie_data = {
                'idMovie': movie.idMovie,
                'dtTitle': movie.dtTitle,
                'dtYear': movie.dtYear,
                'dtAmountOfEp': movie.dtAmountOfEp,
                'dtAmountOfSeasons': movie.dtAmountOfSeasons,
                'dtLength': str(movie.dtLength),
                'dtMinAge': movie.dtMinAge,
                'fiType': movie.fiType,
                'fiGenre': movie.fiGenre,
                'fiLanguage': movie.fiLanguage
            }
            return jsonify(movie_data)

        else:
            movies = Movie.query.all()
            output = []

            for movie in movies:
                movie_data = {
                    'idMovie': movie.idMovie,
                    'dtTitle': movie.dtTitle,
                    'dtYear': movie.dtYear,
                    'dtAmountOfEp': movie.dtAmountOfEp,
                    'dtAmountOfSeasons': movie.dtAmountOfSeasons,
                    'dtLength': str(movie.dtLength),
                    'dtMinAge': movie.dtMinAge,
                    'fiType': movie.fiType,
                    'fiGenre': movie.fiGenre,
                    'fiLanguage': movie.fiLanguage
                }
                output.append(movie_data)

            return jsonify({'movies': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_movie = Movie(**data)

        db.session.add(new_movie)
        db.session.commit()

        return jsonify({'message': 'new movie added'})

    elif request.method == 'PUT':
        data = request.get_json()
        movie = Movie.query.get(id)

        if not movie:
            return jsonify({'message': 'No movie found!'}), 404

        # update attributes
        movie.dtTitle = data.get('dtTitle', movie.dtTitle)

@user.route('/profiles', methods=['GET', 'POST'])
@user.route('/profiles/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_profiles(id=None):
    if request.method == 'GET':
        if id:
            profile = Profile.query.get(id)
            if not profile:
                return jsonify({'message': 'No profile found!'}), 404
            profile_data = {
                'idProfile': profile.idProfile,
                'dtName': profile.dtName,
                'dtMinor': profile.dtMinor,
                'dtProfileImage': profile.dtProfileImage,
                'fiAccount': profile.fiAccount,
                'fiGenre': profile.fiGenre
            }
            return jsonify(profile_data)

        else:
            profiles = Profile.query.all()
            output = []

            for profile in profiles:
                profile_data = {
                    'idProfile': profile.idProfile,
                    'dtName': profile.dtName,
                    'dtMinor': profile.dtMinor,
                    'dtProfileImage': profile.dtProfileImage,
                    'fiAccount': profile.fiAccount,
                    'fiGenre': profile.fiGenre
                }
                output.append(profile_data)

            return jsonify({'profiles': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_profile = Profile(**data)

        db.session.add(new_profile)
        db.session.commit()

        return jsonify({'message':'new profile added'})

    elif request.method == 'PUT':
        data = request.get_json()
        profile = Profile.query.get(id)

        if not profile:
            return jsonify({'message': 'No profile found!'}), 404

        # update attributes
        profile.dtName = data.get('dtName', profile.dtName)


@user.route('/qualities', methods=['GET', 'POST'])
@user.route('/qualities/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_qualities(id=None):
    if request.method == 'GET':
        if id:
            quality = Quality.query.get(id)
            if not quality:
                return jsonify({'message': 'No Quality found!'}), 404
            quality_data = {
                'idType': quality.idType,
                'dtDescription': quality.dtDescription,
                'dtPrice': quality.dtPrice
            }
            return jsonify(quality_data)

        else:
            qualities = Quality.query.all()
            output = []

            for quality in qualities:
                quality_data = {
                    'idType': quality.idType,
                    'dtDescription': quality.dtDescription,
                    'dtPrice': quality.dtPrice
                }
                output.append(quality_data)

            return jsonify({'qualities': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_quality = Quality(**data)

        db.session.add(new_quality)
        db.session.commit()

        return jsonify({'message':'new quality added'})

    elif request.method == 'PUT':
        data = request.get_json()
        quality = Quality.query.get(id)

        if not quality:
            return jsonify({'message': 'No Quality found!'}), 404

        # update attributes
        quality.dtDescription = data.get('dtDescription', quality.dtDescription)
        quality.dtPrice = data.get('dtPrice', quality.dtPrice)

        db.session.commit()

        return jsonify({'message':'Quality updated'})

    elif request.method == 'DELETE':
        quality = Quality.query.get(id)
        if not quality:
            return jsonify({'message': 'No Quality found!'}), 404

        db.session.delete(quality)
        db.session.commit()

        return jsonify({'message':'Quality has been deleted'})

@user.route('/subtitles', methods=['GET', 'POST'])
@user.route('/subtitles/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_subtitles(id=None):
    if request.method == 'GET':
        if id:
            subtitle = Subtitle.query.get(id)
            if not subtitle:
                return jsonify({'message': 'No subtitle found!'}), 404
            subtitle_data = {
                'idSubtitle': subtitle.idSubtitle,
                'fiMovie': subtitle.fiMovie,
                'fiLanguage': subtitle.fiLanguage
            }
            return jsonify(subtitle_data)

        else:
            subtitles = Subtitle.query.all()
            output = []

            for subtitle in subtitles:
                subtitle_data = {
                    'idSubtitle': subtitle.idSubtitle,
                    'fiMovie': subtitle.fiMovie,
                    'fiLanguage': subtitle.fiLanguage
                }
                output.append(subtitle_data)

            return jsonify({'subtitles': output})

    elif request.method == 'POST':
        data = request.get_json()
        new_subtitle = Subtitle(**data)

        db.session.add(new_subtitle)
        db.session.commit()

        return jsonify({'message':'new subtitle added'})

    elif request.method == 'PUT':
        data = request.get_json()
        subtitle = Subtitle.query.get(id)

        if not subtitle:
            return jsonify({'message': 'No subtitle found!'}), 404

        subtitle.fiMovie = data.get('fiMovie', subtitle.fiMovie)
        subtitle.fiLanguage = data.get('fiLanguage', subtitle.fiLanguage)

        db.session.commit()

        return jsonify({'message':'Subtitle updated'})

    elif request.method == 'DELETE':
        subtitle = Subtitle.query.get(id)
        if not subtitle:
            return jsonify({'message': 'No subtitle found!'}), 404

        db.session.delete(subtitle)
        db.session.commit()

        return jsonify({'message':'Subtitle has been deleted'})


@user.route('/views/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_views(id=None):
    if request.method == 'GET':
        if id:  # if id is provided, return a specific view
            view = View.query.get(id)
            if not view:
                return jsonify({'message': 'No View found!'}), 404

            view_data = {
                'idView': view.idView,
                'dtMovieTime': view.dtMovieTime.isoformat(),
                'fiSubtitle': view.fiSubtitle,
                'fiMovie': view.fiMovie,
                'fiProfile': view.fiProfile
            }
            return jsonify(view_data)

        else:  # if id is not provided, return all views
            views = View.query.all()
            output = []
            for view in views:
                view_data = {
                    'idView': view.idView,
                    'dtMovieTime': view.dtMovieTime.isoformat(),
                    'fiSubtitle': view.fiSubtitle,
                    'fiMovie': view.fiMovie,
                    'fiProfile': view.fiProfile
                }
                output.append(view_data)

            return jsonify({'views': output})

    elif request.method == 'POST':
        data = request.get_json()
        # Here you'd typically validate the data format and parameters
        new_view = View(**data)
        new_view.dtMovieTime = datetime.datetime.strptime(data['dtMovieTime'], "%Y-%m-%dT%H:%M:%S")

        db.session.add(new_view)
        db.session.commit()

        return jsonify({'message': 'new view added'})

    elif request.method == 'PUT':
        data = request.get_json()
        view = View.query.get(id)

        if not view:
            return jsonify({'message': 'No View found!'}), 404

        # update attributes
        view.dtMovieTime = datetime.datetime.strptime(data['dtMovieTime'],
                                                      "%Y-%m-%dT%H:%M:%S") if 'dtMovieTime' in data else view.dtMovieTime
        view.fiSubtitle = data.get('fiSubtitle', view.fiSubtitle)
        view.fiMovie = data.get('fiMovie', view.fiMovie)
        view.fiProfile = data.get('fiProfile', view.fiProfile)

        db.session.commit()

        return jsonify({'message': 'View updated'})

    elif request.method == 'DELETE':
        view = View.query.get(id)
        if not view:
            return jsonify({'message': 'No View found!'})



@user.route('/quality')
def test_connection():
    try:

        # Query the first row from the Quality table
        first_row = View.query.first()
        
        if first_row:
            result = f"First row: {first_row.idView}"
        else:
            result = "No records found in dbo.tblQuality"

        return result

    except Exception as e:
        return f"Error: {e}"
