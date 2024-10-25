import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch('app.es')
def test_create_post(mock_es, client):
    mock_es.index.return_value = {'result': 'created'}
    response = client.post('/posts', json={
        'id': 1,
        'title': 'Test Post',
        'content': 'This is a test post'
    })
    assert response.status_code == 201
    assert response.json == {
        'id': 1,
        'title': 'Test Post',
        'content': 'This is a test post'
    }


@patch('app.es')
def test_get_post(mock_es, client):
    mock_es.get.return_value = {
        '_source': {
            'title': 'Test Post',
            'content': 'This is a test post'
        }
    }
    response = client.get('/posts/1/')
    assert response.status_code == 200
    assert response.json == {
        'title': 'Test Post',
        'content': 'This is a test post'
    }


@patch('app.es')
def test_update_post(mock_es, client):
    mock_es.get.return_value = {'_source': {'title': 'Test Post', 'content': 'Old content'}}
    mock_es.update.return_value = {'result': 'updated'}
    response = client.put('/posts/1', json={
        'title': 'Updated Post',
        'content': 'This is updated content'
    })
    assert response.status_code == 200
    assert response.json == {'result': 'updated'}


@patch('app.es')
def test_delete_post(mock_es, client):
    mock_es.get.return_value = {'_source': {'title': 'Test Post', 'content': 'This is a test post'}}
    mock_es.delete.return_value = {'result': 'deleted'}
    response = client.delete('/posts/1')
    assert response.status_code == 200
    assert response.json == {'result': 'deleted'}


@patch('app.es')
def test_search_posts(mock_es, client):
    mock_es.search.return_value = {
        'hits': {
            'hits': [
                {'_source': {'title': 'Test Post 1', 'content': 'Content 1'}},
                {'_source': {'title': 'Test Post 2', 'content': 'Content 2'}}
            ],
            'total': {'value': 2}
        }
    }
    response = client.get('/posts/search?q=test')
    assert response.status_code == 200
    assert response.json == {
        'results': [
            {'title': 'Test Post 1', 'content': 'Content 1'},
            {'title': 'Test Post 2', 'content': 'Content 2'}
        ],
        'total': 2,
        'page': 1,
        'per_page': 5
    }
