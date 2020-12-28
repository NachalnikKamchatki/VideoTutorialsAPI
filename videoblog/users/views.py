from flask import jsonify, Blueprint

from flask_apispec import use_kwargs, marshal_with

from videoblog import session, logger
from videoblog.schemas import UserSchema, AuthSchema
from videoblog.models import User

users = Blueprint('users', __name__)

@users.route('/register', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
    try:
        user = User(**kwargs)
        session.add(user)
        session.commit()
    except Exception as e:
        logger.warning(
            f'Registration failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    token = user.get_token()
    return jsonify({'access_token': token})


@users.route('/login', methods=['POST'])
@use_kwargs(UserSchema(only=('email', 'password')))
@marshal_with(AuthSchema)
def login(**kwargs):
    try:
        user = User.authenticate(**kwargs)
        token = user.get_token()
    except Exception as e:
        logger.warning(
            f'Login action with email {kwargs["email"]} failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    return jsonify({'access_token': token})


@users.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    logger.warning(f'Invalid input params {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


from videoblog import docs
