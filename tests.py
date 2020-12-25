from app import client
from models import *


def test_get_list():
    res = client.get('/tutorials')
    assert res.status_code == 200
    assert len(res.get_json()) == len(Video.query.all())

# {
#         'id': 1,
#         'title': 'Video #1. Intro',
#         'description': 'My first video'
#     },
#     {
#         'id': 2,
#         'title': 'Video #2. Yet one',
#         'description': 'My second video'
#     }


def test_post():
    data = {
        'name': 'Video #1. Intro',
        'description': 'About python'
    }
    res = client.post('/tutorials', json=data)
    assert res.status_code == 200
    assert res.get_json()['name'] == data['name']


def test_put():
    data = {
        'description': 'About python and pythonic way'
    }
    res = client.put('/tutorials/1', json=data)
    assert res.status_code == 200
    assert Video.query.get(1).description == 'About python and pythonic way'


def test_delete():
    res = client.delete('/tutorials/1')
    assert res.status_code == 204
    assert Video.query.get(1) is None
