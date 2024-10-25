<p><h2>Description of the project.</h2><br>
This project is a simple web application on Flask that interacts with Elasticsearch to create, read, update, delete, and search for posts.<br>
The project uses containerization with Docker, which makes it easy to deploy an application with the necessary dependencies.</p>

<p>The main project files are:<br>
app.py:</p>

<p>The main application file on Flask. <br>
The main goal is to provide an API for managing posts using Elasticsearch. <br></p>
<br>

<p><h3>Main functions:</h3> <br>
<strong>Getting posts.</strong> <br>
GET http://localhost:9200/posts/_search</p>

<p><strong>Search for posts by title and content with pagination support.</strong> <br>
GET http://localhost:5001/posts/search?q=world&page=1&per_page=10</p>

<p><strong>Getting a post by ID.</strong> <br>
GET http://localhost:9200/posts/_search</p>

<p>GET http://localhost:5001/posts/search?q=world&page=1&per_page=10</p>

</p>GET http://localhost:9200/posts/_doc/11 <br>
<code>{
        "title": "My eleventh Post",
        "content": "Hello, world!"
}</code>

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
</p>
<p><strong>Creating a new post.</strong> <br>
POST http://localhost:9200/posts/_doc/3 <br>
<code>{
        "title": "My third Post",
        "content": "Hello, world!"
}</code>

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
</p>
<p><strong>Updating an existing post by ID.</strong> <br>
PUT http://localhost:9200/posts/_doc/2 <br>
<code>{
        "title": "My Second Post3",
        "content": "Hello, world!3"
}</code>

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
</p>
<p><strong>Deleting a post by ID.</strong> <br>
DELETE http://localhost:9200/posts/_doc/3 <br>
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
</p>
<p>Elasticsearch is pinged to check availability before launching the application. <br>
All interactions with Elasticsearch are performed using its Python client.</p>


<p><strong>.flake8: </strong><br>
The configuration file for the flake8 tool, which checks the code for compliance with PEP8 standards (Python code style). <br>
Contains rules and exceptions for code validation.</p>


<p><strong>.gitignore: </strong><br>
A list of files and directories that should not be monitored by the Git version control system. <br>
For example, temporary files, generated files, Python environments, etc.</p>


<p><strong>.pylintrc: </strong><br>
The configuration file for the pylint tool, which performs static code analysis. <br>
It contains settings for checking the style, code quality, and various warnings.</p> <br>


<p><strong>docker-compose.yml: </strong><br>
A file for Docker Compose that describes how to run multiple containers at the same time. <br>
Two containers are launched in this project: <br>
    flask_app: A container for a web application on Flask. <br>
    elasticsearch: A container with Elasticsearch for storing and searching data. <br>
Automatically binds containers so that the Flask application can interact with Elasticsearch.</p>


<p><strong>Dockerfile: </strong><br>
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
</p>


<p><strong>mypy.ini: </strong><br>
The configuration file for the mypy tool that checks type annotations in Python. <br>
Helps with static type checking, which improves code quality and helps prevent errors.</p> <br>


<p><strong>pre-commit.sh: </strong><br>
A script for automatically checking the code before committing to Git. <br>
It usually contains commands to run linters, tests, or other code checks before committing changes. <br>
Example: running flake8, pylint, or tests with pytest to make sure that the code meets the standards before making changes to the repository.</p>


<p><strong>Code description: </strong><br>
Application initialization: A Flask application is created, a connection to Elasticsearch is established, and its readiness is checked through the wait_for_elasticsearch function. <br>
<p></p><strong>Routing and API: </strong><br>
    <ul>
        <li>The code implements basic CRUD operations for posts: <br></li>
            <ul>
                <li>Receiving, creating, updating, deleting posts. <br></li>
                <li>Search for posts using full-text search in the title and content fields. <br></li>
            </ul>
        <li>Elasticsearch is used as a data warehouse.</li>
    </li><br>
</p>

Exception handling:<br>
If the document is not found or another error has occurred, an error with the 404 code and description is returned to the client.


<strong>The command to create a container for running tests:</strong><br>
docker-compose run app pytest -v test_blog.py

