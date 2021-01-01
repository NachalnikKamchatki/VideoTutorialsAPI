from flask import jsonify, Blueprint

from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import get_jwt_identity, jwt_required

from videoblog import session, logger, docs
from videoblog.schemas import UserSchema, AuthSchema
from videoblog.models import User
from videoblog.base_view import BaseView

users = Blueprint('users', __name__)


class RegisterView(BaseView):
    @use_kwargs(UserSchema)
    @marshal_with(AuthSchema)
    def post(self, **kwargs):
        try:
            user = User(**kwargs)
            session.add(user)
            session.commit()
        except Exception as e:
            logger.warning(
                f'Registration failed with errors: {str(e)}\n'
            )
            return {'message': str(e)}, 400
        return jsonify({'message': 'success'})


class LoginView(BaseView):
    @use_kwargs(UserSchema(only=('email', 'password')))
    @marshal_with(AuthSchema)
    def post(self, **kwargs):
        try:
            user = User.authenticate(**kwargs)
            token = user.get_token()
        except Exception as e:
            logger.warning(
                f'Login action with email {kwargs["email"]} failed with errors: {str(e)}\n'
            )
            return {'message': str(e)}, 400
        return jsonify({'access_token': token})


class ProfileView(BaseView):
    @jwt_required
    @marshal_with(UserSchema)
    def get(self):
        user_id = get_jwt_identity()
        try:
            user = User.query.get(user_id)
            if not user:
                raise Exception('User not found')
        except Exception as e:
            logger.warning(f'User {user_id}: failed to read profile: {e}')
            return {'message': str(e)}, 400
        return user


RegisterView.register(users, docs, '/register', 'registerview')
LoginView.register(users, docs, '/login', 'loginview')
ProfileView.register(users, docs, '/profile', 'profileview')
