from flask import jsonify, Blueprint, request

from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

from videoblog import logger
from videoblog.schemas import VideoSchema
from videoblog.models import Video
from videoblog.base_view import BaseView

videos = Blueprint('videos', __name__)


class VideoListView(BaseView):
    @jwt_required
    @marshal_with(VideoSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        try:
            videos = Video.get_user_list(user_id=user_id)
        except Exception as e:
            logger.warning(
                f'user {user_id}: tutorials - read action failed with errors: {str(e)}\n'
            )
            return {'message': str(e)}, 400
        return videos

    @jwt_required
    @use_kwargs(VideoSchema)
    @marshal_with(VideoSchema)
    def post(self, **kwargs):
        # создать новое видео для пользователя user_id
        user_id = get_jwt_identity()
        try:
            new_tutorial = Video(user_id=user_id, **kwargs)
            new_tutorial.save_video()
        except Exception as e:
            logger.warning(
                f'user {user_id}: tutorials - create action failed with errors: {str(e)}\n'
            )
            return {'message': str(e)}, 400
        return new_tutorial


class VideoByIdView(BaseView):

    @jwt_required
    # @use_kwargs(VideoSchema)
    @marshal_with(VideoSchema)
    def get(self, tut_id):
        user_id = get_jwt_identity()
        try:
            tutorial = Video.get_video(tut_id=tut_id, user_id=user_id)
        except Exception as e:
            logger.warning(
                f'user {user_id}: tutorial {tut_id} - read action failed with errors: {str(e)}\n'
            )
            return {'message': str(e)}, 400
        return tutorial

    @jwt_required
    @use_kwargs(VideoSchema)
    @marshal_with(VideoSchema)
    def put(self, tut_id, **kwargs):
        # обновить видео video_id для пользователя user_id
        user_id = get_jwt_identity()
        try:
            item = Video.get_video(tut_id, user_id)
            item.update_video(**kwargs)
        except Exception as e:
            logger.warning(
                f'user {user_id}: tutorials {tut_id} - update action failed with errors: {str(e)}\n'
            )
            return {'message': str(e)}, 400
        return jsonify(item)

    @jwt_required
    @marshal_with(VideoSchema)
    def delete(self, tut_id):
        # удалить видео video_id для пользователя user_id
        user_id = get_jwt_identity()
        try:
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


from videoblog import docs

VideoListView.register(videos, docs, '/tutorials', 'videolistview')
VideoByIdView.register(videos, docs, '/tutorials/<int:tut_id>', 'videobyidview')
