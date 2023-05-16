from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models import Actor, Movie
from settings.constants import ACTOR_FIELDS     # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """  
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200) 

  
def get_actor_by_id():
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

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # use this for 200 response code
    try:
        data = data.copy()
        data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
        new_record = Actor.create(**data)
        new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(new_actor), 200)
    except:
        return make_response(jsonify(error='add_actor error'), 400)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # use this for 200 response code
    for k in data:
        if k not in ACTOR_FIELDS:
            return make_response(jsonify(error='update_actor error. wrong fields'), 400)
    try:
        if 'date_of_birth' in data:
            data = data.copy()
            data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
        row_id = int(data['id'])
        upd_record = Actor.update(row_id, **data)
        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(upd_actor), 200)
    except:
        return make_response(jsonify(error='update_actor error'), 400)
    ### END CODE HERE ###

def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # use this for 200 response code
    try:
        if Actor.delete(int(data['id'])) == 1:
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
    except:
        pass
    return make_response(jsonify(error='delete_actor error'), 400)
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    print(data)
    # use this for 200 response code
    try:
        rel_obj = Movie.query.get(int(data['relation_id']))
        actor = Actor.add_relation(int(data['id']), rel_obj)    # add relation here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    except:
        return make_response(jsonify(error='actor_add_relation error'), 400)
    ### END CODE HERE ###


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    try:
    # use this for 200 response code
        actor = Actor.clear_relations(int(data['id']))    # clear relations here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    except:
        return make_response(jsonify(error='actor_clear_relations error'), 400)
    ### END CODE HERE ###