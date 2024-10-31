# import pytest
# from unittest.mock import patch
# from app import app
#
#
# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client
#
#
# @patch('app.es')
# def test_create_post(mock_es, client):
#     mock_es.index.return_value = {'result': 'created'}
#     response = client.post('/posts', json={
#         'id': 1,
#         'title': 'Test Post',
#         'content': 'This is a test post'
#     })
#     assert response.status_code == 201
#     assert response.json == {
#         'id': 1,
#         'title': 'Test Post',
#         'content': 'This is a test post'
#     }
#
#
# @patch('app.es')
# def test_get_post(mock_es, client):
#     mock_es.get.return_value = {
#         '_source': {
#             'title': 'Hello, world!',
#             'content': 'My 33 Post'
#         }
#     }
#     response = client.get('/posts/1')  # убираем конечный слэш
#     assert response.status_code == 200
#     assert response.json == {
#         'title': 'Hello, world!',
#         'content': 'My 33 Post'
#     }
#
#
# @patch('app.es')
# def test_update_post(mock_es, client):
#     mock_es.get.return_value = {'_source': {'title': 'Test Post', 'content': 'Old content'}}
#     mock_es.update.return_value = {'result': 'updated'}
#     response = client.put('/posts/1', json={
#         'title': 'Updated Post',
#         'content': 'This is updated content'
#     })
#     assert response.status_code == 200
#     assert response.json == {'result': 'updated'}
#
#
# @patch('app.es')
# def test_delete_post(mock_es, client):
#     mock_es.get.return_value = {'_source': {'title': 'Test Post', 'content': 'This is a test post'}}
#     mock_es.delete.return_value = {'result': 'deleted'}
#     response = client.delete('/posts/1')
#     assert response.status_code == 200
#     assert response.json == {'result': 'deleted'}
#
#
# @patch('app.es')
# def test_search_posts(mock_es, client):
#     mock_es.search.return_value = {
#         'hits': {
#             'hits': [
#                 {'_source': {'title': 'Test Post 1', 'content': 'Content 1'}},
#                 {'_source': {'title': 'Test Post 2', 'content': 'Content 2'}}
#             ],
#             'total': {'value': 2}
#         }
#     }
#     response = client.get('/posts/search?q=test')
#     assert response.status_code == 200
#     assert response.json == {
#         'results': [
#             {'title': 'Test Post 1', 'content': 'Content 1'},
#             {'title': 'Test Post 2', 'content': 'Content 2'}
#         ],
#         'total': 2,
#         'page': 1,
#         'per_page': 5
#     }


import pytest
from unittest.mock import patch
from app import app
import json
from flask import Flask
from app import create_post


@pytest.fixture
def client1():
    app.config['TESTING'] = True
    with app.test_client() as client1:
        yield client1


@patch('app.es')
def test_get_id(mock_es, client1):
    mock_es.get.return_value = {
        '_id': '1',
        '_source': {
            'title': 'Hello, world!',
            'content': 'My 33 Post'
        }
    }

    response = client1.get('/posts/1')

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response data: {response.data.decode()}"

    assert response.json == {
        '_id': '1',
        'title': 'Hello, world!',
        'content': 'My 33 Post'
    }


@pytest.fixture
def client():
    app = Flask(__name__)
    app.route('/posts/', methods=['POST'])(create_post)
    client = app.test_client()
    return client


@patch('app.es')
def test_create_post_with_id_18(mock_es, client):
    mock_es.search.return_value = {
        'hits': {
            'hits': [{'_id': str(i)} for i in range(1, 18)]
        }
    }

    mock_es.index.return_value = {
        'result': 'created'
    }

    response = client.post('/posts/',
                           data=json.dumps({
                               'title': 'Test Post for ID 18',
                               'content': 'This is a test content for ID 18'
                           }),
                           content_type='application/json')

    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}. Response data: {response.data.decode()}"

    assert response.json == {
        "result": "created",
        "_id": 18
    }

    mock_es.index.assert_called_once_with(index='posts', id=18, body={
        'title': 'Test Post for ID 18',
        'content': 'This is a test content for ID 18'
    })
