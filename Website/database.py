from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)

event_management_db = client['event_management_db']
usersCollection = event_management_db['users']
eventsCollection = event_management_db['events']
