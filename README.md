# Flask REST API to Elasticsearch

This project is a simple web application on Flask that interacts with Elasticsearch to create, read, update, delete, and search for posts.
The project uses containerization with Docker, which makes it easy to deploy an application with the necessary dependencies.


## API

The main application file on Flask. <br>
The main goal is to provide an API for managing posts using Elasticsearch:

* Getting posts. <br>

```GET http://localhost:5001/posts/full```

* Search for posts by title and content with pagination support. <br>

```GET http://localhost:5001/posts/search?q=Hello&page=1&per_page=100```

* Getting a post by ID. <br>

```GET http://localhost:5001/posts/11```

```json
{
        "title": "My eleventh Post",
        "content": "Hello, world!"
}
```
```
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
```

* Creating a new post.

```POST http://localhost:5001/posts```

```
{
        "title": "My third Post",
        "content": "Hello, world!"
}
```

```
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
```

* Updating an existing post by ID. <br>

```PUT http://localhost:5001/posts/2``` <br>

```
{
        "title": "My Second Post3",
        "content": "Hello, world!3"
}
```
```
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
```

* Deleting a post by ID. <br>

```DELETE http://localhost:5001/posts/3``` <br>
```
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
```

Elasticsearch is pinged to check availability before launching the application. <br>
All interactions with Elasticsearch are performed using its Python client. <br>
 <br>

>.flake8:<br>

The configuration file for the flake8 tool, which checks the code for compliance with PEP8 standards (Python code style). <br>
Contains rules and exceptions for code validation.</p> <br>


>.gitignore:<br>

A list of files and directories that should not be monitored by the Git version control system. <br>
For example, temporary files, generated files, Python environments, etc.</p> <br>


>.pylintrc:<br>

The configuration file for the pylint tool, which performs static code analysis. <br>
It contains settings for checking the style, code quality, and various warnings.</p> <br>


>docker-compose.yml:<br>

A file for Docker Compose that describes how to run multiple containers at the same time. <br>
Two containers are launched in this project: <br>
    flask_app: A container for a web application on Flask. <br>
    elasticsearch: A container with Elasticsearch for storing and searching data. <br>
Automatically binds containers so that the Flask application can interact with Elasticsearch.</p> <br>


>Dockerfile:<br>

A script that describes the steps to create a Docker image of a Flask application. <br>
<p></p>Basic steps: <br>
    <ul>
        <li>Uses a basic Python image. <br></li>
        <li>Sets the necessary dependencies from requirements.txt . <br></li>
        <li>Copies the source code of the application to the container. <br></li>
        <li>Launches the Flask application. <br></li>
    </ul>
Example of sections: <br>
    <ul>
        <li>FROM python:3.9: Basic image. <br></li>
        <li>COPY . /app: Copy project files. <br></li>
        <li>RUN pip install -r requirements.txt : Installing dependencies. <br></li>
        <li>CMD ["python", "app.py "]: Launching the application. <br></p></li>
    </ul>
</p> <br>


>mypy.ini:<br>

The configuration file for the mypy tool that checks type annotations in Python. <br>
Helps with static type checking, which improves code quality and helps prevent errors.</p> <br>


>pre-commit.sh:<br>

A script for automatically checking the code before committing to Git. <br>
It usually contains commands to run linters, tests, or other code checks before committing changes. <br>
Example: running flake8, pylint, or tests with pytest to make sure that the code meets the standards before making changes to the repository.</p> <br>


### Code description:<br>

Application initialization: A Flask application is created, a connection to Elasticsearch is established, and its readiness is checked through the wait_for_elasticsearch function.</p> <br>

### Routing and API:<br>
The code implements basic CRUD operations for posts: <br>
        Receiving, creating, updating, deleting posts. <br>
        Search for posts using full-text search in the title and content fields. <br>
Elasticsearch is used as a data warehouse.
<br>


### Exception handling:<br>

If the document is not found or another error has occurred, an error with the 404 code and description is returned to the client.
