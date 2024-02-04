#!/usr/bin/python3
"""
Cities view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def g_cities(state_id):
    '''
    Retrieves the list of all City objects
    related to the state
    '''
    res = storage.get(State, state_id)
    if res is not None:
        return jsonify([state.to_dict() for state in res.cities])
    abort(404)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def g1_city(city_id):
    '''
    Retrieves the City object
    '''
    res = storage.get(City, city_id)
    if res is not None:
        return jsonify(res.to_dict())
    abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """
    Deletes a City object
    """
    res = storage.get(City, city_id)
    if res is not None:
        storage.delete(res)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    Creates a City
    """
    res = storage.get(State, state_id)
    if not res:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in json_data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    name = json_data['name']
    obj = City(name=name)
    obj.state_id = res.id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """
    Updates a City object
    """
    json_data = request.get_json()
    res = storage.get(City, city_id)
    if not res:
        abort(404)
    if not json_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in json_data.items():
        if k not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(res, k, v)
    storage.save()
    return jsonify(res.to_dict())
