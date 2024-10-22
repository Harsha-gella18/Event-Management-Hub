from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .database import usersCollection, eventsCollection
from datetime import datetime
from bson.objectid import ObjectId

# User schema for reference, including registered_events field
usersSchema = {
    "username": None,
    "password": None,
    "email": None,
    "role": None,
    "registered_events": []  # New field for storing registered event IDs
}

# Event schema template including registered_users field
new_event = {
    "title": None,
    "date": None,
    "time": None,
    "location": None,
    "description": None,
    "organizer": None,
    "price": None,
    "TotalCount": None,
    "SlotsLeft": None,
    "registered_users": [],  # New field for storing registered user IDs
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

def get_user(username):
    """
    Get a user by username.
    """
    return usersCollection.find_one({'username': username})

def create_user(username, password_hash, email, role):
    """
    Create a new user in the database.
    """
    data = usersSchema.copy()
    data['username'] = username
    data['password'] = password_hash
    data['email'] = email
    data['role'] = role
    return usersCollection.insert_one(data)

def get_events_by_organizer(organizer_name):
    """
    Fetch events filtered by the organizer's name.
    """
    return list(eventsCollection.find({"organizer": organizer_name}))

def get_events():
    """Fetch all events."""
    return list(eventsCollection.find())

def get_event_by_id(event_id):
    """Fetch an event by its ID."""
    return eventsCollection.find_one({"_id": ObjectId(event_id)})

def add_event(event_data):
    """Add a new event."""
    event = new_event.copy()
    event.update(event_data)
    eventsCollection.insert_one(event)

def update_event(event_id, event_data):
    """Update an event by its ID."""
    event_data['updated_at'] = datetime.utcnow()  # Update timestamp
    eventsCollection.update_one({"_id": ObjectId(event_id)}, {"$set": event_data})

def delete_event(event_id):
    """Delete an event by its ID."""
    eventsCollection.delete_one({"_id": ObjectId(event_id)})

def edit_event_by_id(event_id, event_data):
    """
    Edit an event by its ID.
    
    Parameters:
        event_id (str): The ID of the event to be edited.
        event_data (dict): The data to update in the event.
    
    Returns:
        bool: True if the event was successfully updated, False otherwise.
    """
    try:
        event_data['updated_at'] = datetime.utcnow()  # Update timestamp
        result = eventsCollection.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": event_data}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"An error occurred while editing the event: {e}")
        return False

def delete_event_by_id(event_id):
    """
    Delete an event by its ID.
    
    Parameters:
        event_id (str): The ID of the event to be deleted.
    
    Returns:
        bool: True if the event was successfully deleted, False otherwise.
    """
    try:
        result = eventsCollection.delete_one({"_id": ObjectId(event_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"An error occurred while deleting the event: {e}")
        return False

def register_user_for_event(event_id, user_id):
    """Register a user for an event."""
    try:
        # Retrieve the event
        event = get_event_by_id(event_id)
        print(f"Retrieved event: {event}")

        if event:
            if event['SlotsLeft'] > 0 and user_id not in event.get('registered_users', []):
                # Update the event document
                update_result = eventsCollection.update_one(
                    {"_id": ObjectId(event_id)},
                    {
                        "$addToSet": {"registered_users": user_id},
                        "$inc": {"SlotsLeft": -1}
                    }
                )
                print(f"Event update result: {update_result.modified_count}")

                if update_result.modified_count == 0:
                    print("Failed to update event.")
                    return False

                # Update the user's registered events
                user = get_user_by_id(user_id)
                if user:
                    registered_events = user.get('registered_events', [])
                    if event_id not in registered_events:
                        registered_events.append(event_id)
                        update_result_user = usersCollection.update_one(
                            {'_id': ObjectId(user_id)},
                            {'$set': {'registered_events': registered_events}}
                        )
                        print(f"User update result: {update_result_user.modified_count}")

                        if update_result_user.modified_count == 0:
                            print("Failed to update user.")
                            return False
                        return True
                    else:
                        print("User is already registered for this event.")
            else:
                print("No slots left or user already registered.")
        else:
            print("Event not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False

def unregister_user_from_event(event_id, user_id):
    """Unregister a user from an event."""
    event = get_event_by_id(event_id)
    if event:
        if user_id in event.get('registered_users', []):
            eventsCollection.update_one(
                {"_id": ObjectId(event_id)},
                {
                    "$pull": {"registered_users": user_id},
                    "$inc": {"SlotsLeft": 1}
                }
            )
            # Update user's registered events
            user = get_user_by_id(user_id)
            if user:
                registered_events = user.get('registered_events', [])
                if event_id in registered_events:
                    registered_events.remove(event_id)
                    usersCollection.update_one({'_id': ObjectId(user_id)}, {'$set': {'registered_events': registered_events}})
            return True
    return False

def get_user_by_id(user_id):
    """
    Get a user by their ObjectId.
    """
    return usersCollection.find_one({'_id': ObjectId(user_id)})

def get_user_by_email(email):
    """
    Get a user by their email address.
    """
    return usersCollection.find_one({'email': email})

def reset_user_password(email, new_password):
    """
    Reset the user's password.
    
    Parameters:
        email (str): The email of the user.
        new_password (str): The new password to be set.

    Returns:
        bool: True if the password was successfully reset, False otherwise.
    """
    try:
        # Hash the new password
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        
        # Update the user's password in the database
        result = usersCollection.update_one(
            {'email': email},
            {'$set': {'password': hashed_password}}
        )
        
        # Check if the update was successful
        if result.modified_count > 0:
            return True
        return False
    except Exception as e:
        print(f"An error occurred while resetting the password: {e}")
        return False

def get_all_users():
    """
    Fetches all user documents from the users collection.
    """
    return list(usersCollection.find({'role': 'user'}))

def get_all_admins():
    """
    Fetches all admin documents from the users collection.
    """
    return list(usersCollection.find({'role': 'admin'}))

def get_all_events():
    """
    Fetches all event documents from the events collection.
    """
    return list(eventsCollection.find())

def get_registered_users_for_event(event_id):
    """
    Fetch registered users for a specific event.
    
    Args:
    - event_id (ObjectId): The ID of the event.
    
    Returns:
    - List[dict]: A list of dictionaries containing registered user details.
    """
    try:
        # Fetch the event to get the registered user IDs
        event = eventsCollection.find_one({'_id': ObjectId(event_id)})
        
        if not event:
            return []

        # Get the list of registered user IDs from the event document
        registered_user_ids = event.get('registered_users', [])
        
        if not registered_user_ids:
            return []
        
        # Fetch user details from the users collection
        registered_users = usersCollection.find({'_id': {'$in': registered_user_ids}})
        return list(registered_users)
    except Exception as e:
        print(f"An error occurred while fetching registered users: {e}")
        return []


def delete_user_by_id(user_id):
    try:
        result = usersCollection.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f'Error deleting user: {e}')
        return False

def get_user_by_id(user_id):
    """
    Fetch a user document from the database by user ID.
    
    :param user_id: The ID of the user to retrieve.
    :return: The user document if found, otherwise None.
    """
    try:
        user = usersCollection.find_one({'_id': ObjectId(user_id)})
        return user
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        return None
