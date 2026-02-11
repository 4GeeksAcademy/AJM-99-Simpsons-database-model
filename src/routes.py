from flask import Blueprint, jsonify, request
from sqlalchemy import select
from models import User, Character, Location, db

api = Blueprint("api", __name__)

@api.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    if not characters:
        return jsonify({"error": "There isn't any character yet"}), 404
    response = [character.serialize() for character in characters]
    return jsonify(response), 200

@api.route('/characters', methods=['POST'])
def create_character():
    request_body = request.get_json()
    requested_fields = {"name", "quote", "image"}
    missing = [field for field in requested_fields if field not in request_body]
    if missing:
        return jsonify({"error":"All this character info is missing: {missing}"}), 400
    else:
        new_character = Character (
            name= request_body["name"],
            quote= request_body["quote"],
            image= request_body["image"]
        )
        db.session.add(new_character)
        db.session.commit()
    return jsonify("Character added correctly"),  new_character.serialize(), 200

@api.route('/characters/<int:character_id>', methods=['GET'])
def get_character_id(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "There isn't any character with that id"}), 404
    return jsonify(character.serialize()), 200

@api.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "There isn't any character with that id"}), 404
    request_body = request.get_json()
    for field in ["name", "quote", "image"]:
        if field in request_body:
            setattr(character, field, request_body[field])
    db.session.commit()
    return jsonify(character.serialize()), 200

@api.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "There isn't any character with that id"}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Character deleted correctly"}), 200

@api.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    if not locations:
        return jsonify({"error": "There isn't any location yet"}), 404
    response = [location.serialize() for location in locations]
    return (response, 200)

@api.route('/locations', methods=['POST'])
def create_location():
    request_body = request.get_json()
    requested_fields = {"name", "description", "image"}
    missing = [field for field in requested_fields if field not in request_body]
    if missing:
        return jsonify({"error":"All this location info is missing:" + {missing}}), 400
    else:
        new_location = Location (
            name= request_body["name"],
            description= request_body["description"],
            image= request_body["image"]
        )
        db.session.add(new_location)
        db.session.commit()
    return (jsonify("Location added correctly"),  new_location.serialize(), 201)

@api.route('/locations/<int:location_id>', methods=['GET'])
def get_location_id(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"error": "There isn't any location with that id"}), 404
    return jsonify(location.serialize()), 200

@api.route('/locations/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    locations = Location.query.get(location_id)
    if not locations:
        return jsonify({"error": "There isn't any location with that id"}), 404
    request_body = request.get_json()
    for field in ["name", "description", "image"]:
        if field in request_body:
            setattr(locations, field, request_body[field])
    db.session.commit()
    return jsonify(locations.serialize()), 200

@api.route('/locations/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"error": "There isn't any location with that id"}), 404
    db.session.delete(location)
    db.session.commit()
    return jsonify({"message": "Location deleted correctly"}), 200

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if not users:
        return jsonify({"error": "There isn't any user yet"}), 404
    response = [user.serialize() for user in users]
    return (response, 200)

@api.route('/users', methods=['POST'])
def create_user():
    request_body = request.get_json()
    requested_fields = {"email", "username", "password", "firstname", "lastname"}
    missing = [field for field in requested_fields if field not in request_body]
    if missing:
        return jsonify({"error":"All this user info is missing:" + {missing}}), 400
    else:
        new_user = User (
            username= request_body["username"],
            firstname= request_body["firstname"],
            lastname= request_body["lastname"],
            email= request_body["email"],
            password= request_body["password"],
        )
        db.session.add(new_user)
        db.session.commit()
        return (jsonify("User added correctly"),  new_user.serialize(), 201)

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "There isn't any user with that id"}), 404
    return jsonify(user.serialize()), 200

@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "There isn't any user with that id"}), 404
    request_body = request.get_json()
    for field in ["email", "username", "password", "firstname", "lastname"]:
        if field in request_body:
            setattr(user, field, request_body[field])
    db.session.commit()
    return jsonify(user.serialize()), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "There isn't any user with that id"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted correctly"}), 200

@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = user.query.get(user_id)
    if not user:
        return jsonify({"error": "There isn't any user with that id"}), 404
    fav_characters = [character.serialize() for character in user.fav_characters]
    fav_locations = [location.serialize() for location in user.fav_locations]
    return jsonify(fav_characters,fav_locations), 200

@api.route('/users/<int:user_id>/favorite/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = db.session.execute(select(User).where(User.id==user_id)).scalar_one_or_none()
    character = db.session.execute(select(Character).where(Character.id==character_id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "There isn't any user with that id"}), 404
    if not character:
        return jsonify({"error": "There isn't any character with that id"}), 404
    user.fav_characters.append(character)
    db.session.commit()
    return jsonify({"message": f"{character.name} is now one of the {user.username}'s favorite characters"}), 200

@api.route('/users/<int:user_id>/favorite/characters/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(user_id, character_id):
    user = db.session.execute(select(User).where(User.id==user_id)).scalar_one_or_none()
    character = db.session.execute(select(Character).where(Character.id==character_id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "There isn't any user with that id"}), 404
    if not character:
        return jsonify({"error": "There isn't any character with that id"}), 404
    user.fav_characters.remove(character)
    db.session.commit()
    return jsonify({"message": f"{character.name} is no longer one of the {user.username}'s favorite characters"}), 200

@api.route('/users/<int:user_id>/favorite/locations/<int:location_id>', methods=['POST'])
def add_favorite_location(user_id, location_id):
    user = db.session.execute(select(User).where(User.id==user_id)).scalar_one_or_none()
    location = db.session.execute(select(Location).where(Location.id==location_id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "There isn't any user with that id"}), 404
    if not location:
        return jsonify({"error": "There isn't any location with that id"}), 404
    user.fav_locations.append(location)
    db.session.commit()
    return jsonify({"message": f"{location.name} is now one of the {user.username}'s favorite locations"}), 200

@api.route('/users/<int:user_id>/favorite/locations/<int:location_id>', methods=['DELETE'])
def remove_favorite_location(user_id, location_id):
    user = db.session.execute(select(User).where(User.id==user_id)).scalar_one_or_none()
    location = db.session.execute(select(Location).where(Location.id==location_id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "There isn't any user with that id"}), 404
    if not location:
        return jsonify({"error": "There isn't any location with that id"}), 404
    user.fav_locations.remove(location)
    db.session.commit()
    return jsonify({"message": f"{location.name} is no longer one of the {user.username}'s favorite locations"}), 200

