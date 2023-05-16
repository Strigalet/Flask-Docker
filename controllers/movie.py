from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models import Actor, Movie
from settings.constants import MOVIE_FIELDS     # to make response pretty
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """  
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        act = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(act)
    return make_response(jsonify(movies), 200) 

  
def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # use this for 200 response code
    try:
        new_record = Movie.create(**data)
        new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(new_movie), 200)
    except:
        return make_response(jsonify(error='add_movie error'), 400)
    ### END CODE HERE ###


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    for k in data:
        if k not in MOVIE_FIELDS:
            return make_response(jsonify(error='update_movie error. wrong fields'), 400)
    # use this for 200 response code
    try:
        row_id = int(data['id'])
        upd_record = Movie.update(row_id, **data)
        upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(upd_movie), 200)
    except:
        return make_response(jsonify(error='update_movie error'), 400)
    ### END CODE HERE ###

def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # use this for 200 response code
    try:
        if Movie.delete(int(data['id'])) == 1:
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
    except:
        pass
    return make_response(jsonify(error='delete_movie error'), 400)
    ### END CODE HERE ###


def movie_add_relation():
    """
    Add a movie to movie's cast
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # use this for 200 response code
    try:
        rel_obj = Actor.query.get(int(data['relation_id']))
        movie = Movie.add_relation(int(data['id']), rel_obj)    # add relation here
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    except:
        return make_response(jsonify(error='movie_add_relation error'), 400)
    ### END CODE HERE ###


def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    try:
    # use this for 200 response code
        movie = Movie.clear_relations(int(data['id']))    # clear relations here
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    except:
        return make_response(jsonify(error='movie_clear_relations error'), 400)
    ### END CODE HERE ###