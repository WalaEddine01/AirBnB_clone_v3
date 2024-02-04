#!/usr/bin/python3
""" Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<string:city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves place by its city_id
    """
    city = storage.get(City, city_id)
    if (city is None):
        abort(404)
    place_list_dict = [obj.to_dict() for obj in city.places]
    return jsonify(place_list_dict)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """ Retrieves place object by its id
    """
    place_dct = storage.get(Place, place_id)
    if (place_dct is None):
        abort(404)
    return jsonify(place_dct.to_dict())


@app_views.route("/places/<string:place_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_place_by_id(place_id):
    """ Deletes place by its place_id
    """
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<string:city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create new place object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    json_data = request.get_json()
    user_id = json_data.get('user_id')
    name = json_data.get('name')

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not user_id:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if not name:
        return make_response(jsonify({"error": "Missing name"}), 400)

    json_data['city_id'] = city_id
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    obj = Place(**json_data)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place_by_id(place_id):
    """ Updates place object by its id
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    place_obj = storage.get(Place, place_id)
    if (place_obj is None):
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place_obj, key, value)
    storage.save()
    return jsonify(place_obj.to_dict())
