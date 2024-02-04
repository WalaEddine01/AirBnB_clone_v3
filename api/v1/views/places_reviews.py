#!/usr/bin/python3
"""
place review view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    '''
    Retrieves the list of all Review objects of a Place
    '''
    res = storage.get(Place, place_id)
    if res is not None:
        return jsonify([r.to_dict() for r in res.reviews])
    abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get2_review(review_id):
    '''
    Retrieves a Review object
    '''
    res = storage.get(Review, review_id)
    if res is not None:
        return jsonify(res.to_dict())
    abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(state_id):
    """
    Deletes a State object
    """
    res = storage.get(State, state_id)
    if res is not None:
        storage.delete(res)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/places/<string:place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review
    """
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in json_data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if 'text' not in json_data:
        return make_response(jsonify({"error": "Missing text"}), 400)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    user_id = json_data.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json_data['place_id'] = place_id
    new = Review(**json_data)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/reviews/<string:review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """
    Updates a Review object
    """
    json_data = request.get_json()
    res = storage.get(Review, review_id)
    if not res:
        abort(404)
    if not json_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in json_data.items():
        if k not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(res, k, v)
    storage.save()
    return jsonify(res.to_dict())
