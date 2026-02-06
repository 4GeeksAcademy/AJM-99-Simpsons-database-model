from flask import Blueprint, jsonify
from models import User, Character, Location

api = Blueprint("api", __name__)

@api.route('/people', methods=['GET'])
def get_users():
    users = User.query.all()
    return (jsonify(users), 200)