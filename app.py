import time
from typing import Union, Tuple
import elasticsearch
from flask import Flask, jsonify, request, Response
from elasticsearch import Elasticsearch


app = Flask(__name__)

INDEX_NAME = 'posts'

DATA_FILE = 'data.txt'

es = Elasticsearch(hosts=["http://elasticsearch:9200"])

# pylint: disable=W0621


def wait_for_elasticsearch(es: Elasticsearch) -> None:
    while not es.ping():
        print("Elasticsearch not ready, retrying...")
        time.sleep(5)
    print("Elasticsearch is ready!")


wait_for_elasticsearch(es)


@app.route('/posts/<int:post_id>/', methods=['GET'])
def get_post(post_id: int) -> Union[Response, Tuple[Response, int]]:
    try:
        response = es.get(index=INDEX_NAME, id=str(post_id))
        return jsonify(response['_source'])
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route('/posts', methods=['POST'])
def create_post() -> tuple[Response, int]:
    data = request.get_json()
    post_id = data.get('id')
    title = data.get('title')
    content = data.get('content')

    es.index(index='posts', id=post_id,
             body={'title': title, 'content': content})
    return jsonify({'id': post_id, 'title': title, 'content': content}), 201


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id: int) -> Union[Response, Tuple[Response, int]]:
    data = request.get_json()

    try:
        es.get(index=INDEX_NAME, id=str(post_id))
    except elasticsearch.NotFoundError:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    updated_post = {
        "title": data['title'],
        "content": data['content']
    }

    response = es.update(index=INDEX_NAME, id=str(post_id),
                         body={"doc": updated_post})
    return jsonify({"result": response['result']})


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id: int) -> Union[Response, Tuple[Response, int]]:
    try:
        es.get(index=INDEX_NAME, id=str(post_id))

        response = es.delete(index=INDEX_NAME, id=str(post_id))
        return jsonify({"result": response['result']})
    except elasticsearch.NotFoundError:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404


@app.route('/posts/search', methods=['GET'])
def search_posts() -> Response:
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content"]
            }
        }
    }

    start = (page - 1) * per_page
    response = es.search(index=INDEX_NAME, body=body,
                         from_=start, size=per_page)

    return jsonify({
        "results": [hit["_source"] for hit in response['hits']['hits']],
        "total": response['hits']['total']['value'],
        "page": page,
        "per_page": per_page
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
