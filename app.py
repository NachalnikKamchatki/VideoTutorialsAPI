from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)



@app.route('/tutorials', methods=['GET'])
def get_list():
    videos = Video.query.all()
    serialized = []
    for video in videos:
        serialized.append({
            'id': video.id,
            'name': video.name,
            'description': video.description
        })
    return jsonify(serialized)


@app.route('/tutorials', methods=['POST'])
def update_list():
    new_tutorial = Video(**request.json)
    session.add(new_tutorial)
    session.commit()
    serialised = {
            'id': new_tutorial.id,
            'name': new_tutorial.name,
            'description': new_tutorial.description
    }
    return jsonify(serialised)


@app.route('/tutorials/<int:tut_id>', methods=['PUT'])
def update_item(tut_id):

    item = Video.query.filter(Video.id == tut_id).first()
    params = request.json
    if not item:
        return {'message': 'No tutorials with id.'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialised = {
        'id': item.id,
        'name': item.name,
        'description': item.description
    }
    return jsonify(serialised)


@app.route('/tutorials/<int:tut_id>', methods=['DELETE'])
def delete_item(tut_id):
    item = Video.query.filter(Video.id == tut_id).first()
    if not item:
        return {'message': 'No tutorials with this id.'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)

