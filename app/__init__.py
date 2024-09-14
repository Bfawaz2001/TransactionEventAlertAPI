from flask import Flask

app = Flask(__name__)

# Import the routes after app is initialized to avoid circular imports
from app import routes