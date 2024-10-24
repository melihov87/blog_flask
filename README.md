Description of the project.
This project is a simple web application on Flask that interacts with Elasticsearch to create,
read, update, delete, and search for posts.
The project uses containerization with Docker, which makes it easy to deploy an application with the necessary dependencies.

The main project files are:
app.py:

The main application file on Flask. 
The main goal is to provide an API for managing posts using Elasticsearch. 
Main functions: 

Getting posts. <br>
GET http://localhost:9200/posts/_search

Search for posts by title and content with pagination support. <br>
GET http://localhost:5001/posts/search?q=world&page=1&per_page=10

Getting a post by ID. <br>
GET <http://localhost:9200/posts/_search>

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

Creating a new post. <br>
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

Updating an existing post by ID. <br>
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

Deleting a post by ID. <br>
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

Elasticsearch is pinged to check availability before launching the application.
All interactions with Elasticsearch are performed using its Python client.


.flake8:
The configuration file for the flake8 tool, which checks the code for compliance with PEP8 standards (Python code style).
Contains rules and exceptions for code validation.


.gitignore:
A list of files and directories that should not be monitored by the Git version control system.
For example, temporary files, generated files, Python environments, etc.


.pylintrc:
The configuration file for the pylint tool, which performs static code analysis.
It contains settings for checking the style, code quality, and various warnings.


docker-compose.yml:
A file for Docker Compose that describes how to run multiple containers at the same time.
Two containers are launched in this project:
    flask_app: A container for a web application on Flask.
    elasticsearch: A container with Elasticsearch for storing and searching data.
Automatically binds containers so that the Flask application can interact with Elasticsearch.


Dockerfile: <br>
A script that describes the steps to create a Docker image of a Flask application. <br>
Basic steps: <br>
    <p>Uses a basic Python image. <br><p>
    * Sets the necessary dependencies from requirements.txt . <br>
    Copies the source code of the application to the container. <br>
    Launches the Flask application. <br>
Example of sections: <br>
    FROM python:3.9: Basic image. <br>
    COPY . /app: Copy project files. <br>
    RUN pip install -r requirements.txt : Installing dependencies. <br>
    CMD ["python", "app.py "]: Launching the application. <br>


mypy.ini:
The configuration file for the mypy tool that checks type annotations in Python.
Helps with static type checking, which improves code quality and helps prevent errors.


pre-commit.sh:
A script for automatically checking the code before committing to Git.
It usually contains commands to run linters, tests, or other code checks before committing changes.
Example: running flake8, pylint, or tests with pytest to make sure that the code meets the standards before making changes to the repository.


Code description:
Application initialization: A Flask application is created, a connection to Elasticsearch is established, and its readiness is checked through the wait_for_elasticsearch function.
Routing and API:
    The code implements basic CRUD operations for posts:
        Receiving, creating, updating, deleting posts.
        Search for posts using full-text search in the title and content fields.
    Elasticsearch is used as a data warehouse.
Exception handling: If the document is not found or another error has occurred, an error with the 404 code and description is returned to the client.
