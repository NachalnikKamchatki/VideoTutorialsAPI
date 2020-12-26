from flask import Flask

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from flask_jwt_extended import JWTManager

from flask_apispec.extension import FlaskApiSpec

from config import Config
from logger import init_logger


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

from models import *

Base.metadata.create_all(bind=engine)

logger = init_logger()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


@app.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    logger.warning(f'Invalid input params {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


from routes import *

docs.register(get_list)
docs.register(update_list)
docs.register(update_item)
docs.register(delete_item)
docs.register(register)
docs.register(login)


if __name__ == '__main__':
    app.run(debug=True)
