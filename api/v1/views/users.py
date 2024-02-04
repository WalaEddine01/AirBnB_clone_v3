#!/usr/bin/python3
"""
Users view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all users objects
    """
    return jsonify([user.to_dict() for user in
                    storage.all(User).values()])


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get2_users(user_id):
    """
    Retrieves the list of all users objects
    """
    res = storage.get(User, user_id)
    if res is not None:
        return jsonify(res.to_dict())
    abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """
    Deletes a User object
    """
    res = storage.get(User, user_id)
    if res:
        storage.delete(res)
        storage.save()
        return jsonify({}), 200
    return 404


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a user
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    json_data = request.get_json()

    if 'email' not in json_data:
        return make_response(jsonify({"error": "Missing email"}), 400)

    if 'password' not in json_data:
        return make_response(jsonify({"error": "Missing password"}), 400)

    obj = User(**json_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """
    Updates a User object
    """
    json_data = request.get_json()
    res = storage.get(User, user_id)
    if not res:
        abort(404)
    if not json_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in json_data.items():
        if k not in ["id", "created_at", "updated_at", "email"]:
            setattr(res, k, v)
    storage.save()
    return jsonify(res.to_dict()), 200
