#!/usr/bin/python3
"""
States view
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request


@app_views.route('/python', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<str:state_id>', methods=['GET'],
                 strict_slashes=False)
def states(state_id):
    '''
    Retrieves the list of all State objects
    '''
    if not state_id:
        return storage.get(State)
    res = storage.get(State, state_id)
    if res is not None:
        return res
    return 404


@app_views.route('/states/<str:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_states(state_id):
    """
    Deletes a State object
    """
    res = storage.get(State, state_id)
    if res is not None:
        storage.delete(res)
        return {}, 200
    return 404


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


@app_views.route('/states/<str:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """
    Updates a State object
    """
    json_data = request.get_json()
    res = storage.get(State, state_id)
    if not res:
        return 404
    if not json_data:
        return 'Not a JSON', 400
    for k, v in json_data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(res, k, v)
    storage.save()
    return jsonify(res.to_dict()), 200
