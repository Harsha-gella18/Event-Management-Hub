from datetime import datetime
from app.models.database import eventsCollection, usersCollection
from flask import request, jsonify
from bson import ObjectId


def add_event(data):
    """
    Add a new event to the database.
    """
    try:
        required_fields = ["title", "date", "time", "location", "description", "TotalCount", "EventType", "Points"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"{field} is required"}), 400

        organizer_id = request.user.get("user_id")
        if not organizer_id:
            return jsonify({"error": "Organizer ID is missing"}), 400

        new_event = {
            "title": data["title"],
            "date": data["date"],
            "time": data["time"],
            "location": data["location"],
            "description": data["description"],
            "organizer": organizer_id,
            "price": data.get("price", 0),
            "TotalCount": int(data["TotalCount"]),
            "SlotsLeft": int(data["TotalCount"]),
            "EventType": data["EventType"],
            "Points": int(data["Points"]),
            "registered_users": [],
            "attendees": [],
            "AttendanceTaken": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = eventsCollection.insert_one(new_event)
        return jsonify({"message": "Event added successfully", "event_id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": f"Failed to add event: {str(e)}"}), 500


def get_events():
    """
    Fetch all events created by the admin.
    """
    try:
        organizer_id = request.user.get("user_id")
        if not organizer_id:
            return jsonify({"error": "Organizer ID is missing"}), 400

        # Fetch events from the database
        events = list(eventsCollection.find({"organizer": organizer_id}))

        # Convert ObjectId to string for each event
        for event in events:
            event["_id"] = str(event["_id"])  # Convert ObjectId to string
        print(events)
        print("HarshaVardhan")
        print({"events": events})
        return {"events": list(events)}, 200

    except Exception as e:
        print("Error")
        return jsonify({"error": f"Failed to fetch events: {str(e)}"}), 500

def edit_event(event_id, data):
    """
    Edit an existing event.
    """
    try:
        if not ObjectId.is_valid(event_id):
            return jsonify({"error": "Invalid event ID"}), 400

        event = eventsCollection.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"error": "Event not found"}), 404

        data["updated_at"] = datetime.utcnow()
        eventsCollection.update_one({"_id": ObjectId(event_id)}, {"$set": data})
        return jsonify({"message": "Event updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to edit event: {str(e)}"}), 500


def delete_event(event_id):
    """
    Delete an event.
    """
    try:
        if not ObjectId.is_valid(event_id):
            return jsonify({"error": "Invalid event ID"}), 400

        event = eventsCollection.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"error": "Event not found"}), 404

        eventsCollection.delete_one({"_id": ObjectId(event_id)})
        return jsonify({"message": "Event deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to delete event: {str(e)}"}), 500


def register_for_event(event_id):
    """
    Register a user for an event.
    """
    try:
        if not ObjectId.is_valid(event_id):
            return jsonify({"error": "Invalid event ID"}), 400

        event = eventsCollection.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"error": "Event not found"}), 404

        user_id = request.user.get("user_id")
        if user_id in event.get("registered_users", []):
            return jsonify({"message": "You are already registered for this event"}), 400

        if event["SlotsLeft"] <= 0:
            return jsonify({"message": "No slots left for this event"}), 400

        eventsCollection.update_one(
            {"_id": ObjectId(event_id)},
            {
                "$push": {"registered_users": user_id},
                "$inc": {"SlotsLeft": -1}
            }
        )

        usersCollection.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"registered_events": event_id}}
        )

        return jsonify({"message": "Successfully registered for the event"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to register for event: {str(e)}"}), 500


def get_unregistered_events_for_user():
    """
    Fetch events the user has not registered for.
    """
    try:
        user_id = request.user.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID not found in token"}), 400

        events = list(eventsCollection.find({"registered_users": {"$ne": user_id}}))
        for event in events:
            event["_id"] = str(event["_id"])

        return jsonify({"events": events}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch unregistered events: {str(e)}"}), 500


def get_registered_users(event_id):
    """
    Fetch registered users for a specific event.
    """
    try:
        if not ObjectId.is_valid(event_id):
            return jsonify({"error": "Invalid event ID"}), 400

        event = eventsCollection.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"error": "Event not found"}), 404

        registered_users = list(usersCollection.find({"_id": {"$in": [ObjectId(user_id) for user_id in event.get("registered_users", [])]}}))
        for user in registered_users:
            user["_id"] = str(user["_id"])

        return jsonify({"users": registered_users, "isAttendanceTaken": event.get("AttendanceTaken", False)}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch registered users: {str(e)}"}), 500


def take_attendance(event_id):
    """
    Save attendance for a specific event.
    """
    try:
        if not ObjectId.is_valid(event_id):
            return jsonify({"error": "Invalid event ID"}), 400

        event = eventsCollection.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"error": "Event not found"}), 404

        data = request.json.get("attendance", {})
        attendees = [str(user_id) for user_id, attended in data.items() if attended]

        eventsCollection.update_one(
            {"_id": ObjectId(event_id)},
            {
                "$set": {"AttendanceTaken": True},
                "$addToSet": {"attendees": {"$each": attendees}}
            }
        )

        usersCollection.update_many(
            {"_id": {"$in": attendees}},
            {"$addToSet": {"attended_events": event_id}}
        )

        return jsonify({"message": "Attendance saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to save attendance: {str(e)}"}), 500