from app import client


def test_get_list():
    res = client.get('/tutorials')
    assert res.status_code == 200
    assert res.get_json()[0]['id'] == 1
    assert len(res.get_json())


def test_post():
    data = {
        'id': 3,
        'name': 'Video #3. Strings',
        'description': 'About strings in python'
    }
    res = client.post('/tutorials', json=data)
    assert res.status_code == 200
    assert res.get_json()[2]['id'] == 3
    assert len(res.get_json()) == 3


def test_put():
    data = {
        'description': 'About Strings in python'
    }
    res = client.put('/tutorials/3', json=data)
    assert res.status_code == 200
    assert len(res.get_json()) == 3
    assert 'Strings' in res.get_json()['description']


def test_delete():
    res = client.delete('/tutorials/3')
    assert res.status_code == 204
    assert not res.get_json()
