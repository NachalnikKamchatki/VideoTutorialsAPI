import sqlalchemy as db
from sqlalchemy.orm import relationship

from flask_jwt_extended import create_access_token
from datetime import timedelta

from passlib.hash import bcrypt

from . import Base, session


class Video(Base):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @classmethod
    def get_user_videos(cls, user_id):
        try:
            videos = cls.query.filter(cls.user_id == user_id).all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return videos

    @classmethod
    def get_video(cls, tut_id, user_id):
        try:
            item = cls.query.filter(cls.id == tut_id, cls.user_id == user_id).first()
            if not item:
                raise Exception('No tutorials with this id')
        except Exception:
            session.rollback()
            raise
        return item

    def save_video(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def update_video(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete_video(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def __repr__(self):
        return f'<Video {self.name}>'


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    videos = relationship('Video', backref='user', lazy=True)

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expires_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id,
            expires_delta=expires_delta
        )
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not user:
            raise Exception('No user with this email')
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user

    def __repr__(self):
        return f'<User {self.name}>'
