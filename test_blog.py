import requests
import json


def test_view_posts_id():
    url = "http://localhost:5001/posts/15"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    print(response.status_code)


# ====================================================================================
def test_view_posts_full():
    url = "http://localhost:5001/posts/full"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# ====================================================================================
def test_view_posts_search():
    url = "http://localhost:5001/posts/search?q=Hello&page=1&per_page=100"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# ====================================================================================
def test_create_posts():
    url = "http://localhost:5001/posts"

    payload = json.dumps({
      "title": "My 18 Post",
      "content": "Hello, world!"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# ====================================================================================
def test_update_posts():
    url = "http://localhost:5001/posts/17"

    payload = json.dumps({
      "title": "My 17 Post",
      "content": "Hello, world!"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)


# ====================================================================================
def test_delete_posts():
    url = "http://localhost:5001/posts/16"

    payload = {}
    headers = {}

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response.text)
