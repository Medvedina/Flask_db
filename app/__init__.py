from flask import Flask
from config import Config
from flask_jwt_extended import JWTManager
import os


app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)