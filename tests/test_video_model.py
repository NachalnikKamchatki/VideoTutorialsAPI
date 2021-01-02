def test_model(video):
    assert video.name == 'Test Video'


def test_get_user_video_list(video, client, user_headers):
    res = client.get('/tutorials', headers=user_headers)
    assert res.status_code == 200
    assert len(res.get_json()) == 1
    assert res.get_json()[0] == {
        'description': 'Just test video',
        'id': 1,
        'name': 'Test Video',
        'user_id': 1
    }


def test_new_video(video, user, client, user_headers):
    res = client.post('/tutorials', json={
        'name': 'Test Video 2',
        'description': 'Yet one test video'
    }, headers=user_headers)
    assert res.status_code == 200
    assert res.get_json()['name'] == 'Test Video 2'
    assert res.get_json()['user_id'] == user.id


def test_edit_video(video, client, user_headers):
    res = client.put(f'/tutorials/{video.id}',
        json={
            'name': 'Test Video updated',
            'description': 'Updated'
        },
        headers=user_headers)
    assert res.status_code == 200


def test_delete_video(video, client, user_headers):
    res = client.delete(f'/tutorials/{video.id}', headers=user_headers)
    assert res.status_code == 204
