from flask import Flask

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

jwt = JWTManager(app)

docs = FlaskApiSpec()
docs.init_app(app)

from .models import *

Base.metadata.create_all(bind=engine)

logger = init_logger()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


from videoblog.main.views import *
from videoblog.users.views import *

app.register_blueprint(videos)
app.register_blueprint(users)

docs.register(get_list, blueprint='videos')
docs.register(update_list, blueprint='videos')
docs.register(update_item, blueprint='videos')
docs.register(delete_item, blueprint='videos')
docs.register(register, blueprint='users')
docs.register(login, blueprint='users')


