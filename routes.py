from flask import jsonify

from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import app, session, logger
from schemas import *
from models import *


@app.route('/tutorials', methods=['GET'])
@jwt_required
@marshal_with(VideoSchema(many=True))
def get_list():
    try:
        user_id = get_jwt_identity()
        videos = Video.query.filter(Video.user_id == user_id).all()
    except Exception as e:
        logger.warning(
            f'user {user_id}: tutorials - read action failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    return videos


@app.route('/tutorials', methods=['POST'])
@jwt_required
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_list(**kwargs):
    try:
        user_id = get_jwt_identity()
        new_tutorial = Video(user_id=user_id, **kwargs)
        session.add(new_tutorial)
        session.commit()
    except Exception as e:
        logger.warning(
            f'user {user_id}: tutorials - create action failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    return new_tutorial


@app.route('/tutorials/<int:tut_id>', methods=['PUT'])
@jwt_required
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_item(tut_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        item = Video.query.filter(Video.id == tut_id,
                                  Video.user_id == user_id).first()
        if not item:
            return {'message': 'No tutorials with id.'}, 400
        for key, value in kwargs.items():
            setattr(item, key, value)
        session.commit()
    except Exception as e:
        logger.warning(
            f'user {user_id}: tutorials {tut_id} - update action failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    return jsonify(item)


@app.route('/tutorials/<int:tut_id>', methods=['DELETE'])
@jwt_required
@marshal_with(VideoSchema)
def delete_item(tut_id):
    try:
        user_id = get_jwt_identity()
        item = Video.query.filter(Video.id == tut_id,
                                  Video.user_id == user_id).first()
        if not item:
            return {'message': 'No tutorials with this id.'}, 400
        session.delete(item)
        session.commit()
    except Exception as e:
        logger.warning(
            f'user {user_id}: tutorials {tut_id} - delete action failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    return '', 204


@app.route('/register', methods=['POST'])
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


@app.route('/login', methods=['POST'])
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


from app import docs
