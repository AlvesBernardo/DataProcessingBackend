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
from app.extensions import call_stored_procedure_post ,call_stored_procedure_get
user_route = Blueprint('user', __name__)
s = URLSafeTimedSerializer('secret')
play_count = {}
@user_route.route('/users', methods=['GET', 'POST'])
@user_route.route('/users/<id>', methods=['GET', 'POST', 'DELETE'])
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

        new_classification_data = (data['dtEmail'],data['dtPassword'],data['fiSubscription'],data['fiLanguage'])
        end_message = call_stored_procedure_post("""InsertAccount
                                                            @dtEmail = ? ,
                                                            @dtPassword = ? ,
                                                            @fiSubscription = ? , 
                                                            @fiLanguage = ? """, new_classification_data)
        if end_message == []:
            return jsonify({'message': 'new account added'})
        else:
            return jsonify({'message': 'account could not be added', 'error_message': end_message})
    # Throws an error even if it works
    elif request.method == 'DELETE':
        user = Account.query.get(id)
        error_message = call_stored_procedure_post("DeleteAccountAndRelatedContent @AccountID = ? ",(id,))
        if error_message == []:
            return jsonify({'message': 'account deleted'})
        else:
            return jsonify({'message': 'account could not be deleted', 'error_message': error_message})



@user_route.route('/subscriptions', methods=['GET', 'POST'])
@user_route.route('/subscriptions/<id>', methods=['GET', 'POST', 'DELETE'])
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
        data = request.get_json()
        new_profile_data = (data['Payment'], data['DateOfSignUp'],data['QualityType'])
        end_message = call_stored_procedure_post("""InsertSubscription
                                                                                    @Payment = ?,
                                                                                    @DateOfSignUp = ?,
                                                                                    @QualityType = ? 
                                                                                    """, new_profile_data)
        if end_message == []:
            return jsonify({'message': 'new quality added'})
        else:
            return jsonify({'message': 'quality could not be added', 'error_message': end_message})
        return jsonify({'message':'new subscription added'})

    elif request.method == 'DELETE':
        subscription = Subcription.query.get(id)
        if not subscription:
            return jsonify({'message': 'No subscription found!'}), 404

        db.session.delete(subscription)
        db.session.commit()

        return jsonify({'message':'subscription has been deleted'})

@user_route.route('/languages', methods=['GET', 'POST'])
@user_route.route('/languages/<id>', methods=['GET', 'POST', 'DELETE'])
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
        new_subscription_data = (data['dtDescription'])
        end_message = call_stored_procedure_post("""InsertLanguage
                                                            @dtDescription = ?
                                                            
                                                        """,
                                                 new_subscription_data)
        if end_message == []:
            return jsonify({'message': 'new Language added'})
        else:
            return jsonify({'message': 'Language could not be added', 'error_message': end_message})


    elif request.method == 'DELETE':
        language = Language.query.get(id)
        if not language:
            return jsonify({'message': 'No language found!'}), 404

        db.session.delete(language)
        db.session.commit()

        return jsonify({'message': 'language has been deleted'})

@user_route.route('/profiles', methods=['GET', 'POST'])
@user_route.route('/profiles/<id>', methods=['GET', 'PUT', 'DELETE'])
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
        new_language_data = (data['Name'],data['IsMinor'],data['ProfileImage'],data['IsAccountDisabled'],data['AccountID'],data['Genre']
                             )
        end_message = call_stored_procedure_post("""InsertProfile
                                                                            @Name = ? ,
                                                                            @IsMinor = ?,
                                                                            @ProfileImage = ?,
                                                                            @IsAccountDisabled = ? ,
                                                                            @AccountID = ? , 
                                                                            @Genre = ? 
                                                                            """, new_language_data)
        if end_message == []:
            return jsonify({'message': 'new profile added'})
        else:
            return jsonify({'message': 'profile could not be added', 'error_message': end_message})

    elif request.method == 'PUT':
        data = request.get_json()
        profile = Profile.query.get(id)

        if not profile:
            return jsonify({'message': 'No profile found!'}), 404

        # update attributes
        profile.dtName = data.get('dtName', profile.dtName)





@user_route.route('/views',methods = ['GET','POST'])
@user_route.route('/views/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
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
        new_profile_data = (data['SubtitleID'], data['MovieID'],data['ProfileID'],data["MovieTime"])
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





@user_route.route('/quality')
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
