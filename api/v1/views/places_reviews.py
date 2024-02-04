#!/usr/bin/python3
""" Place Review module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<string:place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_all_review(place_id):
    """ Retrieves all places review by its place_id
    """
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)
    review_list_dict = [obj.to_dict() for obj in place.reviews]
    return jsonify(review_list_dict)


@app_views.route('/review/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """ Retrieves review by its id
    """
    review = storage.get(Review, review_id)
    if (review is None):
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<string:review_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_review_by_id(review_id):
    """ Deletes review by its id
    """
    review = storage.get(Review, review_id)
    if (review is None):
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<string:place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create new review object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    json_data = request.get_json()
    user_id = json_data.get('user_id')
    text = json_data.get('text')

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not user_id:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if not text:
        return make_response(jsonify({"error": "Missing text"}), 400)

    json_data['place_id'] = place_id
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    obj = Review(**json_data)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """ Updates review object by its id
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    review_obj = storage.get(Review, review_id)
    if (review_obj is None):
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict())
