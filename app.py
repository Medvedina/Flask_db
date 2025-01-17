from dotenv import load_dotenv
load_dotenv()

import os

from flask import jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager
from app.routes import auth_bp
from app import app

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)