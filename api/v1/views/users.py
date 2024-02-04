#!/usr/bin/python3
""" User module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_user():
    """ Retrieves all user
    """
    users_list = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(users_list)


@app_views.route("/users/<string:user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieves user by its id
    """
    user = storage.get(User, user_id)
    if (user is None):
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_user_by_id(user_id):
    """ Deletes user by its id
    """
    user = storage.get(User, user_id)
    if (user is None):
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """ Create new user
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    json_data = request.get_json()

    if 'email' not in json_data:
        return make_response(jsonify({"error": "Missing email"}), 400)

    if 'password' not in json_data:
        return make_response(jsonify({"error": "Missing password"}), 400)

    # email = json_data['email']
    # password = json_data['password']
    # obj = User(email=email, password=password)
    obj = User(**json_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<string:user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user_by_id(user_id):
    """ Updates user object by its id
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_obj = storage.get(User, user_id)
    if (user_obj is None):
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user_obj, key, value)
    storage.save()
    return jsonify(user_obj.to_dict())