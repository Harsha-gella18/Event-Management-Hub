from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import Blueprints
from app.Routes.authroutes import auth_blueprint
from app.Routes.eventroutes import event_blueprint

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend communication

    # Secret Key for JWT
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "DEFAULT_SECRET_KEY")

    # Register Blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(event_blueprint, url_prefix='/events')

    return app
