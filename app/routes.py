from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.repository import get_repository

    
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
        return jsonify(message="Неверные учетные данные"), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    full_name = data.get('full_name')
    birth_date = data.get('birth_date') if data.get('birth_date') != '' else None

    if repo.register_user(login, password, full_name, birth_date):
        return jsonify(message="Пользователь успешно зарегистрирован."), 201
    else:
        return jsonify(message="Ошибка при регистрации пользователя."), 400


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    current_user_login = get_jwt()['login']

    return jsonify(logged_in_as=current_user_login, user_id=current_user_id), 200
