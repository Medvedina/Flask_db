from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.repository import get_repository
from app.models.account import RegistrateDTO
    
auth_bp = Blueprint('auth_bp', __name__)
repo = get_repository()


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    user = repo.get_user(login, password)

    if user:
        access_token = create_access_token(identity=str(user[0]), additional_claims={'login': user[1]})
        return jsonify(access_token=access_token), 200
    else:
        return '', 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    account = RegistrateDTO(**data)

    if repo.register_user(account):
        return jsonify(message=f"Пользователь {account.login} успешно зарегистрирован."), 201
    else:
        return jsonify(message="Имя пользователя уже используется"), 400


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    current_user_login = get_jwt()['login']

    return '', 201