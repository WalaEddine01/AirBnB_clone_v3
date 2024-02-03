#!/usr/bin/python3
"""
place review view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    '''
    Retrieves the list of all Review objects of a Place
    '''
    res = storage.get(Place, place_id)
    if res is not None:
        return jsonify(r.to_dict() for r in res.reviews)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def states(place_id):
    '''
    Retrieves a Place object
    '''
    res = storage.get(City, place_id)
    if res is not None:
        return jsonify(res.to_dict())
    abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_states(state_id):
    """
    Deletes a State object
    """
    res = storage.get(State, state_id)
    if res is not None:
        storage.delete(res)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a State
    """
    json_data = request.get_json()
    if not json_data:
        return "Not a JSON", 400
    if 'name' not in json_data:
        return "Missing name", 400
    new = State(**json_data)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """
    Updates a State object
    """
    json_data = request.get_json()
    res = storage.get(State, state_id)
    if not res:
        abort(404)
    if not json_data:
        return 'Not a JSON', 400
    for k, v in json_data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(res, k, v)
    storage.save()
    return jsonify(res.to_dict()), 200
