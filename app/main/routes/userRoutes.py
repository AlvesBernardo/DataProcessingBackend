from app.extensions import db
from flask import Blueprint, request, jsonify
from itsdangerous import URLSafeTimedSerializer
from app.models.account_model import Account
from app.models.language_model import Language
from app.models.profile_model import Profile
from app.models.subscription_model import Subcription
from app.models.view_model import View
from app.models.watchList_model import WatchList
from app.services.auth_guard import check_jwt_token
import datetime
from app.services.auth_guard import auth_guard
from app.extensions import call_stored_procedure_post, call_stored_procedure_get

user_route = Blueprint('user', __name__)
s = URLSafeTimedSerializer('secret')
play_count = {}


@user_route.route('/users', methods=['GET', 'POST'])
@user_route.route('/users/<id>', methods=['GET', 'POST', 'DELETE'])
@auth_guard('admin')
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

        new_classification_data = (data['dtEmail'], data['dtPassword'], data['fiSubscription'], data['fiLanguage'])
        end_message = call_stored_procedure_post("""InsertAccount
                                                                @dtEmail = ? ,
                                                                @dtPassword = ? ,
                                                                @fiSubscription = ? , 
                                                                @fiLanguage = ? """, new_classification_data)
        if not end_message:
            return jsonify({'message': 'new account added'})
        else:
            return jsonify({'message': 'account could not be added', 'error_message': end_message})
    elif request.method == 'DELETE':
        user = Account.query.get(id)
        error_message = call_stored_procedure_post("DeleteAccountAndRelatedContent @AccountID = ? ", (id,))
        if not error_message:
            return jsonify({'message': 'account deleted'})
        else:
            return jsonify({'message': 'account could not be deleted', 'error_message': error_message})


@user_route.route('/subscriptions', methods=['GET', 'POST'])
@user_route.route('/subscriptions/<id>', methods=['GET', 'POST', 'DELETE'])
@auth_guard
def manage_subscriptions(id=None):
    if request.method == 'GET':
        current_user_id = check_jwt_token()

        account_details = call_stored_procedure_get("""
                                                                        GetAccountDetails
                                                                        @AccountID = ?
                                                                    """,
                                                    (current_user_id,))
        if not account_details:
            return jsonify({'message': 'Account details not found.'}), 404
        account_details = account_details[0]

        response = {
            'idAccount': account_details[0],
            'dtEmail': account_details[1],
            'dtPassword': account_details[2],
            'dtPayment': account_details[3],
            'dtDateOfSignUp': account_details[4],
            'dtSubscriptionPrice': account_details[5],
            'dtDescription': account_details[6]
        }

        return jsonify(response)
    elif request.method == 'POST':
        data = request.get_json()
        data = request.get_json()
        new_profile_data = (data['Payment'], data['DateOfSignUp'], data['QualityType'])
        end_message = call_stored_procedure_post("""InsertSubscription
                                                                @Payment = ?,
                                                                @DateOfSignUp = ?,
                                                                @QualityType = ? 
                                                                """, new_profile_data)
        if not end_message:
            return jsonify({'message': 'new quality added'})
        else:
            return jsonify({'message': 'quality could not be added', 'error_message': end_message})
        return jsonify({'message': 'new subscription added'})
    elif request.method == 'DELETE':
        subscription = Subcription.query.get(id)
        if not subscription:
            return jsonify({'message': 'No subscription found!'}), 404
        db.session.delete(subscription)
        db.session.commit()

        return jsonify({'message': 'subscription has been deleted'})


@user_route.route('/languages', methods=['GET', 'POST'])
@user_route.route('/languages/<id>', methods=['GET', 'POST', 'DELETE'])
@auth_guard('admin')
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
        new_subscription_data = (data['dtDescription'])
        end_message = call_stored_procedure_post("""InsertLanguage
                                                                    @dtDescription = ?
                                                                """,
                                                 new_subscription_data)
        if not end_message:
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
@auth_guard('admin')
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
        new_language_data = (
            data['Name'], data['IsMinor'], data['ProfileImage'], data['IsAccountDisabled'], data['AccountID'],
            data['Genre']
        )
        end_message = call_stored_procedure_post("""InsertProfile
                                                                @Name = ? ,
                                                                @IsMinor = ?,
                                                                @ProfileImage = ?,
                                                                @IsAccountDisabled = ? ,
                                                                @AccountID = ? , 
                                                                @Genre = ? 
                                                                """, new_language_data)
        if not end_message:
            return jsonify({'message': 'new profile added'})
        else:
            return jsonify({'message': 'profile could not be added', 'error_message': end_message})
    elif request.method == 'PUT':
        data = request.get_json()
        profile = Profile.query.get(id)

        if not profile:
            return jsonify({'message': 'No profile found!'}), 404
        profile.dtName = data.get('dtName', profile.dtName)


@user_route.route('/views', methods=['GET', 'POST'])
@user_route.route('/views/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth_guard('admin')
def manage_views(id=None):
    if request.method == 'GET':
        if id:
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
        else:
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
        new_profile_data = (data['SubtitleID'], data['MovieID'], data['ProfileID'], data["MovieTime"])
        end_message = call_stored_procedure_post("""InsertView
                                                                @SubtitleID = ?,
                                                                @MovieID = ? ,
                                                                @ProfileID = ? ,
                                                                @MovieTime = ? 
                                                                """, new_profile_data)
        if not end_message:
            return jsonify({'message': 'new view added'})
        else:
            return jsonify({'message': 'view could not be added', 'error_message': end_message})
    elif request.method == 'PUT':
        data = request.get_json()
        view = View.query.get(id)

        if not view:
            return jsonify({'message': 'No View found!'}), 404

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


@user_route.route('/watchlist', methods=['GET', 'POST'])
@user_route.route('/watchlist/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth_guard('admin')
def handle_watchlist(id=None):
    if request.method == 'GET':
        if id:
            watchlist = WatchList.query.get(id)
            if watchlist is None:
                return jsonify(f'Watchlist with Id {id} does not exist'), 404
            return jsonify(watchlist.serialize())
        else:
            watchlist = WatchList.query.all()
            return jsonify([e.serialize() for e in watchlist])
    elif request.method == 'POST':
        data = request.get_json()
        new_watchlist_data = (data['fiMovie'], data['fiProfile'])
        end_message = call_stored_procedure_post("""InsertWatchList
                                                                @MovieID = ? ,
                                                                @ProfileID = ? """,
                                                 new_watchlist_data)
        if not end_message:
            return jsonify({'message': 'new watchlist added'}), 201
        else:
            return jsonify({'message': 'watchlist could not be added', 'error_message': end_message})
    elif request.method == 'PUT':
        data = request.get_json()
        watchlist = WatchList.query.get(id)
        if 'fiMovie' in data:
            watchlist.fiMovie = data['fiMovie']
        if 'fiProfile' in data:
            watchlist.fiProfile = data['fiProfile']
        db.session.commit()
        return jsonify(watchlist.serialize())
    elif request.method == 'DELETE':
        watchlist = WatchList.query.get(id)
        if watchlist is None:
            return jsonify(f'Watchlist with Id {id} does not exist'), 404
        db.session.delete(watchlist)
        db.session.commit()
        return '', 204
    else:
        return jsonify(f'Invalid request method'), 405
