#!/usr/bin/python3
""" Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenity():
    """ Retrieves all amenity
    """
    amenities_list = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(amenities_list)


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """ Retrieves amenity by its id
    """
    amenity = storage.get(Amenity, amenity_id)
    if (amenity is None):
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity_by_id(amenity_id):
    """ Deletes amenity by its id
    """
    amenity = storage.get(Amenity, amenity_id)
    if (amenity is None):
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Create new amenity object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    json_data = request.get_json()

    if 'name' not in json_data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    name = json_data['name']
    obj = Amenity(name=name)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """ Updates amenity object by its id
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    amenity_obj = storage.get(Amenity, amenity_id)
    if (amenity_obj is None):
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, key, value)
    storage.save()
    return jsonify(amenity_obj.to_dict())
