from flask import Flask, jsonify, request

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

from models import *

Base.metadata.create_all(bind=engine)


@app.route('/tutorials', methods=['GET'])
@jwt_required
def get_list():
    user_id = get_jwt_identity()
    videos = Video.query.filter(Video.user_id == user_id)
    serialized = []
    for video in videos:
        serialized.append({
            'id': video.id,
            'name': video.name,
            'description': video.description
        })
    return jsonify(serialized)


@app.route('/tutorials', methods=['POST'])
@jwt_required
def update_list():
    user_id = get_jwt_identity()
    new_tutorial = Video(user_id=user_id, **request.json)
    session.add(new_tutorial)
    session.commit()
    serialised = {
            'id': new_tutorial.id,
            'name': new_tutorial.name,
            'description': new_tutorial.description
    }
    return jsonify(serialised)


@app.route('/tutorials/<int:tut_id>', methods=['PUT'])
@jwt_required
def update_item(tut_id):
    user_id = get_jwt_identity()
    item = Video.query.filter(Video.id == tut_id,
                              Video.user_id == user_id).first()
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
@jwt_required
def delete_item(tut_id):
    user_id = get_jwt_identity()
    item = Video.query.filter(Video.id == tut_id,
                              Video.user_id == user_id).first()
    if not item:
        return {'message': 'No tutorials with this id.'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return jsonify({
        'status': 'success',
        'access_token': token}
    )


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    return jsonify({'access=token': token})


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)

