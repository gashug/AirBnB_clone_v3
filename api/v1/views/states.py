#!/usr/bin/python3
""" States API routes """
from flask import Flask, request, abort, jsonify
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route("/states/", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve a list of all State objects"""
    states = storage.all("State").values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route("/state/", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieve a State object by ID"""
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route(
        "/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Remove a State object by ID"""
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    """Create new State Object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["put"], strict_slashes=False)
def update_state():
    """Upadate a specific State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    data.pop('id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
