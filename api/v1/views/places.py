#!/usr/bin/python3
"""
Place view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(city_id):
    '''
    Retrieves the list of all Place objects of a City
    '''
    city = storage.get(City, city_id)
    if (city is None):
        abort(404)
    place_list_dict = [obj.to_dict() for obj in city.places]
    return jsonify(place_list_dict)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get2_place(place_id):
    '''
    Retrieves a Place object
    '''
    place_dct = storage.get(Place, place_id)
    if (place_dct is None):
        abort(404)
    return jsonify(place_dct.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """
    Deletes a Place object
    """
    res = storage.get(Place, place_id)
    if res is not None:
        storage.delete(res)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place
    """
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in json_data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in json_data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    user = storage.get(User, json_data['user_id'])
    if user is None:
        abort(404)
    json_data['city_id'] = city_id
    new_place = Place(**json_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """
    Updates a Place object
    """
    json_data = request.get_json()
    res = storage.get(Place, place_id)
    if not res:
        abort(404)
    if not json_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in json_data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(res, k, v)
    storage.save()
    return jsonify(res.to_dict())
