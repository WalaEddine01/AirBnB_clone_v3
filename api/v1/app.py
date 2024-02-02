#!/usr/bin/python3
"""
Web server
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import getenv
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
HOST = getenv("HBNB_API_HOST", default="0.0.0.0")
API = getenv("HBNB_API_PORT", default="5000")


@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    # python -m api.v1.app
    app.run(host=HOST, port=API, threaded=True)
