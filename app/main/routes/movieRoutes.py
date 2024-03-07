from app.extensions import db
from app.extensions import call_stored_procedure_get , call_stored_procedure_post
from flask import Blueprint, request, jsonify,Response
from itsdangerous import URLSafeTimedSerializer
from app.models.genre_model import Genre
from app.models.movie_model import Movie
from app.models.quality_model import Quality
from app.models.subtitle_model import Subtitle
from app.services.auth_guard import auth_guard
import io
import csv
from dateutil.parser import parse
movie_routes = Blueprint('movies', __name__)
s = URLSafeTimedSerializer('secret')
play_count = {}
def convert_to_csv(header:list,data:list) :
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(header)
    cw.writerows(data)
    return si.getvalue()
@movie_routes.route('/classifications', methods=['GET', 'POST'])
@movie_routes.route('/classifications/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_classifications(id=None):
    if request.method == 'GET':
        # Example GET logic
        if id:
            # Logic to get a specific classification
            classification_data = {'id': id, 'description': 'Example Classification'}
        else:
            # Logic to get all classifications
            classification_data = [{'id': 1, 'description': 'Classification 1'},
                                   {'id': 2, 'description': 'Classification 2'}]

        # Check 'Accept' header for response type
        if 'text/csv' in request.headers.get('Accept', ''):
            # Convert response data to CSV
            data = [[classification['id'], classification['description']] for classification in classification_data]
            output = convert_to_csv(['id', 'description'],data)
            return Response(output, mimetype='text/csv')
        else:
            # Return JSON
            return jsonify(classification_data)

    elif request.method == 'POST':
        # Example POST logic
        if request.content_type == 'text/csv':
            # Handle CSV data
            csv_file = request.files['file']
            # Process CSV data
        elif request.content_type == 'application/json':
            data = request.get_json()
            # Process JSON data
        return jsonify({'message': 'Classification added or updated'})

    elif request.method == 'PUT':
        # Example PUT logic (similar to POST)
        data = request.get_json()  # Assuming JSON data
        # Update classification logic
        return jsonify({'message': 'Classification updated'})

    elif request.method == 'DELETE':
        # Example DELETE logic
        # Delete classification logic
        return jsonify({'message': 'Classification deleted'})

    else:
        # Handle other HTTP methods or return error
        return jsonify({'message': 'Method not allowed'}), 405


@auth_guard('admin')
@movie_routes.route('/genres', methods=['GET', 'POST'])
@movie_routes.route('/genres/<id>', methods=['GET', 'PUT', 'DELETE'])
def manage_genres(id=None):
    if request.method == 'GET':
        # GET logic
        if id:
            # Logic to get a specific genre
            genre = Genre.query.get(id)
            if not genre:
                return jsonify({'message': 'No genre found!'}), 404
            genre_data = {'idGenre': genre.idGenre, 'dtDescription': genre.dtDescription}
        else:
            # Logic to get all genres
            genres = Genre.query.all()
            genre_data = [{'idGenre': genre.idGenre, 'dtDescription': genre.dtDescription} for genre in genres]

        # Response type handling
        if 'text/csv' in request.headers.get('Accept', ''):
            
            data = [[genre['idGenre'], genre['dtDescription']] for genre in genre_data]
            output = convert_to_csv(['idGenre', 'dtDescription'], data)
            return Response(output, mimetype='text/csv')
        else:
            return jsonify({'genres': genre_data})

    elif request.method == 'POST':
        if request.content_type == 'text/csv':
            csv_file = request.files['file']
            # Process CSV data
        elif request.content_type == 'application/json':
            data = request.get_json()
            # Process JSON data
        return jsonify({'message': 'Genre added'})

    elif request.method == 'PUT':
        data = request.get_json()
        genre = Genre.query.get(id)
        if not genre:
            return jsonify({'message': 'No genre found!'}), 404
        # Update logic
        genre.dtDescription = data['dtDescription']
        db.session.commit()
        return jsonify({'message': 'Genre updated'})

    elif request.method == 'DELETE':
        genre = Genre.query.get(id)
        if not genre:
            return jsonify({'message': 'No genre found!'}), 404
        db.session.delete(genre)
        db.session.commit()
        return jsonify({'message': 'Genre deleted'})

    else:
        return jsonify({'message': 'Method not allowed'}), 405
    
@movie_routes.route('/movies', methods=['GET', 'POST'])
@movie_routes.route('/movies/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth_guard()
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
                'fiClassification': movie.fiClassification,
                'fiLanguage': movie.fiLanguage
            }
            return jsonify(movie_data)

        else:
            movies = call_stored_procedure_get(procedure_name="GetAllMovies")
            return jsonify({'movies': movies})

    elif request.method == 'POST':
        data = request.get_json()
        new_language_data = (data['dtTitle'], parse(data['dtYear']),data['dtAmountOfEP'],data['dtAmountOfSeasons'],
                             parse(data['dtLength']) ,
                             data['dtMinAge'],data['fiType'],data['fiLanguage'],data['fiClassification'],data['fiGenre'],)
        end_message = call_stored_procedure_post("""InsertNewMovie 
                                                                    @dtTitle = ? ,
                                                                    @dtYear = ? ,
                                                                    @dtAmountOfEp = ?,
                                                                    @dtAmountOfSeasons = ? ,
                                                                    @dtLength = ? ,
                                                                    @dtMinAge = ? , 
                                                                    @fiType = ? ,
                                                                    @fiLanguage = ?,
                                                                    @fiClassification = ?,
                                                                    @fiGenre = ? 
                                                                    """, new_language_data)
        if end_message == []:
            return jsonify({'message': 'new movie added'})
        else:
            return jsonify({'message': 'movie could not be added', 'error_message': end_message})
    elif request.method == 'PUT':
        data = request.get_json()
        movie = Movie.query.get(id)
        if not movie:
            return jsonify({'message': 'No movie found!'}), 404

        # update attributes
        movie.dtTitle = data.get('dtTitle', movie.dtTitle)
    elif request.method == 'DELETE' :
        end_message = call_stored_procedure_post("DeleteMovieAndRelatedContent @MovieID = ? ", (id,))
        if end_message == []:
            return jsonify({'message': 'movie deleted'})
        else:
            return jsonify({'message': 'movie could not be deleted', 'error_message': end_message})
@movie_routes.route('/qualities', methods=['GET', 'POST'])
@movie_routes.route('/qualities/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth_guard()
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
        new_profile_data  =  (data['dtDescription'],data['dtPrice'])
        end_message = call_stored_procedure_post("""InsertQuality
                                                                            @dtDescription = ?,
                                                                            @dtPrice = ?
                                                                            """, new_profile_data)
        if end_message == []:
            return jsonify({'message': 'new quality added'})
        else:
            return jsonify({'message': 'quality could not be added', 'error_message': end_message})
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
@movie_routes.route('/subtitles', methods=['GET', 'POST'])
@movie_routes.route('/subtitles/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth_guard()
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
            subtitles = call_stored_procedure_get("GetAllSubtitles")

            return jsonify({'subtitles': subtitles})

    elif request.method == 'POST':
        data = request.get_json()

        new_subscription_data = (data['fiMovie'],data['fiLanguage'])
        end_message = call_stored_procedure_post("""InsertSubtitle
                                                    @fiMovie = ?,
                                                    @fiLanguage = ?
                                                """,
                                                 new_subscription_data)
        if end_message == []:
            return jsonify({'message': 'new Subtitle added'})
        else:
            return jsonify({'message': 'Subtitle could not be added', 'error_message': end_message})

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

        return jsonify({'message':'Subtitle has been deleted'})