from flask import Flask

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from flask_jwt_extended import JWTManager

from flask_apispec.extension import FlaskApiSpec

from .config import Config
from .logger import init_logger


app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager()

docs = FlaskApiSpec()


from .models import *

Base.metadata.create_all(bind=engine)

logger = init_logger()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


from videoblog.main.views import videos
from videoblog.users.views import users


app.register_blueprint(videos)
app.register_blueprint(users)

docs.init_app(app)
jwt.init_app(app)
