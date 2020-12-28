from flask import jsonify, Blueprint

from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

from videoblog import logger
from videoblog.schemas import VideoSchema
from videoblog.models import Video

videos = Blueprint('videos', __name__)


@videos.route('/tutorials', methods=['GET'])
@jwt_required
@marshal_with(VideoSchema(many=True))
def get_list():
    try:
        user_id = get_jwt_identity()
        videos = Video.get_user_videos(user_id=user_id)
    except Exception as e:
        logger.warning(
            f'user {user_id}: tutorials - read action failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    return videos


@videos.route('/tutorials', methods=['POST'])
@jwt_required
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_list(**kwargs):
    try:
        user_id = get_jwt_identity()
        new_tutorial = Video(user_id=user_id, **kwargs)
        new_tutorial.save_video()
    except Exception as e:
        logger.warning(
            f'user {user_id}: tutorials - create action failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    return new_tutorial


@videos.route('/tutorials/<int:tut_id>', methods=['PUT'])
@jwt_required
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_item(tut_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        item = Video.get_video(tut_id, user_id)
        item.update_video(**kwargs)
    except Exception as e:
        logger.warning(
            f'user {user_id}: tutorials {tut_id} - update action failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    return jsonify(item)


@videos.route('/tutorials/<int:tut_id>', methods=['DELETE'])
@jwt_required
@marshal_with(VideoSchema)
def delete_item(tut_id):
    try:
        user_id = get_jwt_identity()
        item = Video.get_video(tut_id, user_id)
        if not item:
            return {'message': 'No tutorials with this id.'}, 400
        item.delete_video()
    except Exception as e:
        logger.warning(
            f'user {user_id}: tutorials {tut_id} - delete action failed with errors: {str(e)}\n'
        )
        return {'message': str(e)}, 400
    return '', 204


@videos.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    logger.warning(f'Invalid input params {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


from videoblog import docs
