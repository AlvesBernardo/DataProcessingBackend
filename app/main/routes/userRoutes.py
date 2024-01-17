from app.config.connection_configuration import engine
from app.services.emailSender import send_email
from app.extensions import db
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


@user.route('/sendEmail')
def sendingEmail(recieverEmail, subject, body):
    """
    Sends an email to the specified receiver email address.

    :param recieverEmail: The email address of the receiver.
    :param subject: The subject of the email.
    :param body: The body content of the email.
    :return: None
    """
    send_email(recieverEmail, subject, body)


@user.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Sends a password reset email to the user.

    :return: A JSON response indicating the status of the password reset request.
    """
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
    """
    Reset Password

    Resets the password for a user.

    :param token: The token used for password reset.
    :return: A JSON response with a message indicating the result of the password reset.
    """
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
    """
    This method `manage_users` handles various HTTP methods and operations related to user management.

    :param id: Optional parameter representing the user ID. If provided, returns details of a specific user. If not provided, returns details of all users.
    :return: Returns JSON response containing user data or appropriate message.

    """
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
    """
    This function is used to manage subscriptions of a user. It handles HTTP GET, POST, and DELETE request methods for the '/subscriptions' route.

    .. code-block:: python

        @user.route('/subscriptions', methods=['GET', 'POST'])
        @user.route('/subscriptions/<id>', methods=['GET', 'POST', 'DELETE'])
        def manage_subscriptions(id=None):

    Parameters:
        - id (optional): The ID of the subscription to retrieve or delete.

    Returns:
        - If the request method is GET:
            - If an ID is provided, it returns the subscription data as a JSON response.
            - If no ID is provided, it returns all the subscriptions as a JSON response.
        - If the request method is POST:
            - It creates a new subscription based on the data provided in the request's JSON payload. Returns a JSON response with a success message.
        - If the request method is DELETE:
            - Deletes the subscription with the provided ID. Returns a JSON response with a success message.

    Note:
        - This function assumes that some external resources (e.g., database) are accessible and used for operations like fetching, creating, and deleting subscriptions.
        - The code snippet provided here is just an example and may need to be modified to fit your specific application.
        - The properties to be included in the subscription data should be added or customized as per your requirements.
        - The route decorators and other framework-specific details are omitted from the docstring for simplicity.

    """
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


@user.route('/languages', methods=['GET', 'POST'])
@user.route('/languages/<id>', methods=['GET', 'POST', 'DELETE'])
def manage_languages(id=None):
    """
    This method, `manage_languages`, is used to manage languages in a user API. It handles HTTP GET, POST, and DELETE requests for language resources.

    :param id: An optional parameter specifying the ID of the language to be manipulated. If provided, the method retrieves or deletes a specific language identified by the ID. If not provided
    *, the method retrieves all languages.
    :return: The method returns JSON data representing the language(s) depending on the request type.

    **HTTP GET Request**:
    - If an `id` is provided:
        - If a language with the specified ID exists, the method retrieves it from the database and returns its details in JSON format.
        - If no language with the specified ID exists, a JSON response with an error message and HTTP status code 404 (Not Found) is returned.
    - If no `id` is provided:
        - All languages stored in the database are retrieved and returned as a list of JSON objects, each representing a language.

    **HTTP POST Request**:
    - The method expects a JSON payload containing the data required to create a new language instance (e.g., `{'idLanguage': 'eng', 'dtDescription': 'English'}`).
    - The new language data is saved to the database using SQLAlchemy ORM.
    - The method returns a JSON response with a success message indicating that the new language has been added.

    **HTTP DELETE Request**:
    - If an `id` is provided:
        - If a language with the specified ID exists, it is removed from the database using SQLAlchemy ORM.
        - If no language with the specified ID exists, a JSON response with an error message and HTTP status code 404 (Not Found) is returned.
    - The method returns a JSON response with a success message indicating that the language has been deleted.

    **Note**: The method assumes that the Flask application is already set up, and the necessary imports and configurations are in place.
    """
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

        return jsonify({'message':'new language added'})

    elif request.method == 'DELETE':
        language = Language.query.get(id)
        if not language:
            return jsonify({'message': 'No language found!'}), 404

        db.session.delete(language)
        db.session.commit()

        return jsonify({'message':'language has been deleted'})


@user.route('/classifications', methods=['GET', 'POST'])
@user.route('/classifications/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_classifications(id=None):
    """
    API endpoint for managing classifications.

    :param id: Optional parameter to specify the ID of a specific classification.
    :return: JSON response with the requested classification(s) information.

    GET method:
        If `id` is provided, returns the classification information for the specified ID.
        If `id` is not provided, returns the information for all classifications.

    POST method:
        Adds a new classification to the database based on the provided JSON data.
        Returns a JSON response with a success message.

    PUT method:
        Updates the classification information for the specified ID based on the provided JSON data.
        Returns a JSON response with a success message.

    DELETE method:
        Deletes the classification with the specified ID from the database.
        Returns a JSON response with a success message.

    """
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
    """
    Manage Genres

    Handles various operations related to genres.

    :param id: The ID of the genre to manage. Defaults to None.
    :return: Returns the result of the operation as JSON.

    """
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
    """
    Handles CRUD operations for movies.

    :param id: (int, optional) The ID of the movie to manage.
    :return: (json) The requested movie data or a list of all movies.
    """
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
    """
    Endpoint for managing profiles.

    :param id: Optional. The id of the profile to manage.
    :return: JSON response with requested profile data or list of profiles.
    """
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
    """
    Manage Qualities

    This method manages qualities based on the HTTP request method. It supports GET, POST, PUT, and DELETE operations.

    :param id: The ID of the quality (optional)
    :return: JSON response with quality data or a message

    GET Method:
    If an ID is provided, it retrieves the specific quality with the given ID. If no quality is found, a 404 error is returned.
    If no ID is provided, it retrieves all qualities from the database and returns them as a list of JSON objects.

    POST Method:
    Creates a new quality using the JSON data provided in the request payload. The new quality is then added to the database.
    Returns a JSON response with a success message.

    PUT Method:
    Updates an existing quality with the provided ID. The JSON data in the request payload is used to update the specified attributes of the quality.
    If no quality is found with the given ID, a 404 error is returned.
    Returns a JSON response with a success message.

    DELETE Method:
    Deletes an existing quality with the provided ID.
    If no quality is found with the given ID, a 404 error is returned.
    Returns a JSON response with a success message.

    """
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
    """
    Manage subtitles.

    :param id: The ID of the subtitle to manage (optional).
    :return: If id is provided, returns the details of the specified subtitle.
             If id is not provided, returns a list of all subtitles.
    :rtype: JSON

    """
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
    """
    :param id: The ID of the view to be managed. If provided, it returns a specific view. If not provided, it returns all views.
    :return: If id is provided, returns a specific view in JSON format. If id is not provided, returns all views in JSON format.
    """
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






