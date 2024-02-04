#!/usr/bin/python3
""" City module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_citie(state_id):
    """ Retrieves city by its state_id
    """
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)
    city_list_dict = [obj.to_dict() for obj in state.cities]
    return jsonify(city_list_dict)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """ Retrieves city object by its id
    """
    city_dct = storage.get(City, city_id)
    if (city_dct is None):
        abort(404)
    return jsonify(city_dct.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_city_by_id(city_id):
    """ Deletes city by its city_id
    """
    city = storage.get(City, city_id)
    if (city is None):
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<string:state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Create new city object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    state = storage.get(State, state_id)
    if (state is None):
        abort(404)

    json_data = request.get_json()

    if 'name' not in json_data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    """ obj = City(**json_data)
    obj.state_id = state.id
    obj.save() """
    name = json_data['name']
    obj = City(name=name)
    obj.state_id = state.id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city_by_id(city_id):
    """ Updates city object by city_id
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    city_obj = storage.get(City, city_id)
    if (city_obj is None):
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city_obj, key, value)
    storage.save()
    return jsonify(city_obj.to_dict())
