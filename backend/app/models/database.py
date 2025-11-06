from pymongo import MongoClient, ASCENDING
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)

# Database
event_management_db = client['event_management_db']

# Collections
usersCollection = event_management_db['users']
eventsCollection = event_management_db['events']

# Ensure indexing for performance
usersCollection.create_index([("email", ASCENDING)], unique=True)
usersCollection.create_index([("username", ASCENDING)], unique=True)
eventsCollection.create_index([("title", ASCENDING)])