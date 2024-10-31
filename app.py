import time
from typing import Tuple
from flask import Flask, jsonify, request, Response
from elasticsearch import Elasticsearch, NotFoundError
from typing import Union


app = Flask(__name__)

INDEX_NAME = 'posts'
es = Elasticsearch(hosts=["http://elasticsearch:9200"])


def wait_for_elasticsearch(es: Elasticsearch) -> None:
    while not es.ping():
        print("Elasticsearch not ready, retrying...")
        time.sleep(5)
    print("Elasticsearch is ready!")


wait_for_elasticsearch(es)


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id: int) -> Union[Response, Tuple[Response, int]]:
    try:
        response = es.get(index=INDEX_NAME, id=str(post_id))

        post = {"_id": response["_id"], **response["_source"]}

        return jsonify(post), 200
    except NotFoundError:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/posts/full', methods=['GET'])
def get_all_posts() -> Union[Response, Tuple[Response, int]]:
    per_page = int(request.args.get('per_page', 10000))
    try:
        response = es.search(index=INDEX_NAME, size=per_page, body={"query": {"match_all": {}}})

        posts = [{"_id": hit["_id"], **hit["_source"]} for hit in response['hits']['hits']]

        sorted_results = sorted(
            [
                {
                    "id": int(hit["_id"]),
                    **hit["_source"]
                } for hit in response['hits']['hits']
            ],
            key=lambda x: x["id"]
        )

        return jsonify({
            "results": sorted_results,
            "total": response['hits']['total']['value'],
            "per_page": per_page
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/posts/', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = {
        "title": data['title'],
        "content": data['content']
    }

    try:
        search_body = {
            "_source": False,
            "query": {"match_all": {}},
            "sort": [{"_id": "asc"}],
            "size": 10000
        }
        response = es.search(index=INDEX_NAME, body=search_body)
        existing_ids = sorted([int(hit["_id"]) for hit in response['hits']['hits']])

        current_id = 1
        for eid in existing_ids:
            if eid == current_id:
                current_id += 1
            else:
                break

        response = es.index(index=INDEX_NAME, id=current_id, body=new_post)
        return jsonify({"result": response['result'], "_id": current_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id: int) -> Union[Response, Tuple[Response, int]]:
    data = request.get_json()
    if not data or not all(k in data for k in ("title", "content")):
        return jsonify({"error": "Missing required fields: title and content"}), 400

    updated_post = {
        "title": data['title'],
        "content": data['content']
    }

    try:
        es.update(index=INDEX_NAME, id=str(post_id), body={"doc": updated_post})
        return jsonify({"message": "Post updated successfully"}), 200
    except NotFoundError:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    try:
        res = es.delete(index=INDEX_NAME, id=id)
        return jsonify({"result": "deleted", "id": res['_id']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route('/posts/search', methods=['GET'])
def search_posts() -> Union[Response, Tuple[Response]]:
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

    try:
        start = (page - 1) * per_page
        response = es.search(index=INDEX_NAME, body=body, from_=start, size=per_page)

        sorted_results = sorted(
            [
                {
                    "id": int(hit["_id"]),
                    **hit["_source"]
                } for hit in response['hits']['hits']
            ],
            key=lambda x: x["id"]
        )

        return jsonify({
            "results": sorted_results,
            "total": response['hits']['total']['value'],
            "page": page,
            "per_page": per_page
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
