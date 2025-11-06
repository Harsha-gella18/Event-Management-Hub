from flask import Blueprint, request, jsonify
from app.models.events import (
    add_event,
    edit_event,
    delete_event,
    get_events,
    register_for_event,
    get_unregistered_events_for_user,
    get_registered_users,
    take_attendance,
)
from app.utils import token_required, admin_required, user_required

# Define the blueprint for event-related routes
event_blueprint = Blueprint('event', __name__)

@event_blueprint.route('/add_event', methods=['POST'])
@token_required
@admin_required
def add_new_event():
    """
    Route to add a new event. Only accessible by admins.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is missing"}), 400
        return add_event(data)
    except Exception as e:
        return jsonify({"error": f"Failed to add event: {str(e)}"}), 500


@event_blueprint.route('/edit_event/<event_id>', methods=['PUT'])
@token_required
@admin_required
def edit_the_event(event_id):
    """
    Route to edit an existing event. Only accessible by admins.
    """
    try:
        if not event_id:
            return jsonify({"error": "Event ID is required"}), 400
        data = request.json
        if not data:
            return jsonify({"error": "Request body is missing"}), 400
        return edit_event(event_id, data)
    except Exception as e:
        return jsonify({"error": f"Failed to edit event: {str(e)}"}), 500


@event_blueprint.route('/delete_event/<event_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_the_event(event_id):
    """
    Route to delete an event. Only accessible by admins.
    """
    try:
        if not event_id:
            return jsonify({"error": "Event ID is required"}), 400
        return delete_event(event_id)
    except Exception as e:
        return jsonify({"error": f"Failed to delete event: {str(e)}"}), 500


@event_blueprint.route('/admin/get_events', methods=['GET'])
@token_required
@admin_required
def fetch_admin_events():
    """
    Route to fetch all events created by the admin.
    """
    try:
        return get_events()
    except Exception as e:
        return jsonify({"error": f"Failed to fetch events: {str(e)}"}), 500


@event_blueprint.route('/user/register/<event_id>', methods=['POST'])
@token_required
@user_required
def register_for_event_route(event_id):
    """
    Route for a user to register for an event.
    """
    try:
        if not event_id:
            return jsonify({"error": "Event ID is required"}), 400
        return register_for_event(event_id)
    except Exception as e:
        return jsonify({"error": f"Failed to register for event: {str(e)}"}), 500


@event_blueprint.route('/user/unregistered_events', methods=['GET'])
@token_required
@user_required
def fetch_unregistered_events():
    """
    Route to fetch events that the user has not registered for.
    """
    try:
        return get_unregistered_events_for_user()
    except Exception as e:
        return jsonify({"error": f"Failed to fetch unregistered events: {str(e)}"}), 500


@event_blueprint.route('/<event_id>/registered_users', methods=['GET'])
@token_required
@admin_required
def fetch_registered_users(event_id):
    """
    Route to fetch users registered for a specific event.
    """
    try:
        if not event_id:
            return jsonify({"error": "Event ID is required"}), 400
        return get_registered_users(event_id)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch registered users: {str(e)}"}), 500


@event_blueprint.route('/<event_id>/take_attendance', methods=['POST'])
@token_required
@admin_required
def take_event_attendance(event_id):
    """
    Route to take attendance for a specific event.
    """
    try:
        if not event_id:
            return jsonify({"error": "Event ID is required"}), 400
        return take_attendance(event_id)
    except Exception as e:
        return jsonify({"error": f"Failed to take attendance: {str(e)}"}), 500