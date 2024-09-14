from flask import request, jsonify
from app import app

user_actions = {}


@app.route('/event', methods=['POST'])
def event():
    data = request.json
    user_id = data['user_id']

    # Process data and return response (from the earlier implementation)
    # ...