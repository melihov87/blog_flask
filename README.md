GET http://localhost:9200/posts/_search

GET http://localhost:5001/posts/search?q=world&page=1&per_page=10

GET http://localhost:9200/posts/_doc/11
    {
        "title": "My eleventh Post",
        "content": "Hello, world!"
    }

        {
            "_index": "posts",
            "_type": "_doc",
            "_id": "11",
            "_version": 2,
            "result": "updated",
            "_shards": {
                "total": 2,
                "successful": 1,
                "failed": 0
            },
            "_seq_no": 111,
            "_primary_term": 36
        }

POST http://localhost:9200/posts/_doc/3
    {
        "title": "My third Post",
        "content": "Hello, world!"
    }

        {
        "_index": "posts",
        "_type": "_doc",
        "_id": "3",
        "_version": 2,
        "result": "updated",
        "_shards": {
            "total": 2,
            "successful": 1,
            "failed": 0
        },
        "_seq_no": 116,
        "_primary_term": 36
    }

PUT http://localhost:9200/posts/_doc/2
    {
        "title": "My Second Post3",
        "content": "Hello, world!3"
    }

        {
            "_index": "posts",
            "_type": "_doc",
            "_id": "2",
            "_version": 2,
            "result": "updated",
            "_shards": {
                "total": 2,
                "successful": 1,
                "failed": 0
            },
            "_seq_no": 112,
            "_primary_term": 36
        }

DELETE http://localhost:9200/posts/_doc/3
    {
        "_index": "posts",
        "_type": "_doc",
        "_id": "3",
        "_version": 2,
        "result": "deleted",
        "_shards": {
            "total": 2,
            "successful": 1,
            "failed": 0
        },
        "_seq_no": 113,
        "_primary_term": 36
    }
