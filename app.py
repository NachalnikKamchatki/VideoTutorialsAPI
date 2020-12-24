from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# session.create_all()

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)

tutorials = [
    {
        'id': 1,
        'title': 'Video #1. Intro',
        'description': 'My first video'
    },
    {
        'id': 2,
        'title': 'Video #2. Yet one',
        'description': 'My second video'
    }
]


@app.route('/tutorials', methods=['GET'])
def get_list():
    return jsonify(tutorials)


@app.route('/tutorials', methods=['POST'])
def update_list():
    new_tutorial = request.json
    tutorials.append(new_tutorial)
    return jsonify(tutorials)


@app.route('/tutorials/<int:tut_id>', methods=['PUT'])
def update_item(tut_id):

    item = next((x for x in tutorials if x['id'] == tut_id), None)
    params = request.json
    if not item:
        return {'message': 'No tutorials with id.'}, 400
    item.update(params)
    return jsonify(item)


@app.route('/tutorials/<int:tut_id>', methods=['DELETE'])
def delete_item(tut_id):

    indx, _ = next((x for x in enumerate(tutorials) if x[1]['id'] == tut_id), (None, None))

    if not indx:
        return {'message': 'No tutorials with this id.'}, 400

    tutorials.pop(indx)
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)

