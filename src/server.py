from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'super-secret'

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
    password = data.get('password')
    firstname = data.get('firstname')
    lastname = data.get('lastname')

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
        ), 401
    if not current_user.check_password(password):
        return jsonify({'message': 'Bad password'}), 401

    token = create_access_token(identity=username)
    return jsonify(token=token), 200


# Эндпойнт для получения списка всех пользователей
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.username for user in users]), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
