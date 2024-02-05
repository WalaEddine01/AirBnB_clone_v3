#!/usr/bin/python3
"""
view for the link between Place objects and Amenity objects that handles
all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
