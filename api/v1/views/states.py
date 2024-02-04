#!/usr/bin/python3
""" State module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_state():
    """ Retrieves all state objects
    """
    states_list = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route("/states/<string:state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """ Retrieves state by its state_id
    """
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state_by_id(state_id):
    """ Deletes state by its state_id
    """
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """ Create new state object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    json_data = request.get_json()

    if 'name' not in json_data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    name = json_data['name']
    obj = State(name=name)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=['PUT'],
                 strict_slashes=False)
def update_state_by_id(state_id):
    """ Updates state object by its state_id
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state_obj = storage.get(State, state_id)
    if (state_obj is None):
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)
    storage.save()
    return jsonify(state_obj.to_dict())
