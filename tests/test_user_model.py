
def test_model(user):
    assert user.name == 'TestUser'


def test_user_login(user, client):
    res = client.post('/login', json={
        'email': user.email,
        'password': 'password'
    })
    assert res.status_code == 200
    assert res.get_json().get('access_token')


def test_user_register(client):
    res = client.post('/register', json={
        'name': 'TestUser',
        'email': 'test@test.ua',
        'password': 'password'
    })
    assert res.status_code == 200
    assert res.get_json().get('message') == 'success'


def test_user_profile(client, user_headers):
    res = client.get('/profile', headers=user_headers)
    assert res.status_code == 200
    assert res.get_json().get('name') == 'TestUser'
    assert res.get_json().get('videos') == []