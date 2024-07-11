from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

MIN_PASSWORD_LENGTH = 3


# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Эндпойнт для регистрации нового пользователя
@ app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify(
            {'message': 'User with that username is already exists'}
        ), 400
    if not username:
        return jsonify({'message': 'Username is missing'}), 400
    if not password:
        return jsonify({'message': 'Password is missing'}), 400
    if len(password) < MIN_PASSWORD_LENGTH:
        return jsonify(
            {'message':
             f'Password must be at least {MIN_PASSWORD_LENGTH} characters'}
        ), 400

    new_user = User(username=username, firstname=firstname, lastname=lastname)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User successfully created'}), 201


# Эндпойнт для авторизации пользователя
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    current_user = User.query.filter_by(username=username).first()

    if current_user is None:
        return jsonify(
            {'message': 'User with that username was not found'}
        ), 400
    if not current_user.check_password(password):
        return jsonify({'message': 'Bad password'}), 400

    token = create_access_token(identity=username)
    return jsonify(token=token), 200


# Эндпойнт для получения всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users_list), 200


# Эндпойнт для получения информации о конкретном пользователе
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User was not found'}), 404

    user_data = {
        'id': user.id,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname
    }
    return jsonify(user_data), 200


# Эндпойнт для обновления информации о пользователе
@app.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User was not found'}), 404

    data = request.json
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    password = data.get('password')

    if firstname:
        user.firstname = firstname
    if lastname:
        user.lastname = lastname
    if password:
        user.set_password(password)
    db.session.commit()
    return jsonify({'message': 'User updated'}), 200


# Эндпойнт для удаления пользователя
@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User was not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200


# Заглушка для начальной страницы
@app.route('/')
def hello_world():
    return 'Easy Server'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
