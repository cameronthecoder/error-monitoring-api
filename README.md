# Error Monitoring API
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository contains the backend code for the error monitoring project.

## Table of contents
- [Error Monitoring API](#error-monitoring-api)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
    - [Framework and Packages](#framework-and-packages)
    - [How to run the app](#how-to-run-the-app)
    - [Contributions](#contributions)
    - [API Documentation](#api-documentation)
    - [Roadmap](#roadmap)

## Overview

### Framework and Packages
This API uses the following framework and extensions:
- [Quart](https://pgjones.gitlab.io/quart/index.html) - Quart is an ASGI Python microframework similar to [Flask](https://flask.palletsprojects.com/en/2.0.x/). Quart supports full asynchronous code.
- [Quart-Schema](https://pgjones.gitlab.io/quart-schema/) - Quart-Schema is an extension for the Quart microframework. It allows validation of incoming and outgoing data (usually JSON) against a Python [dataclass](https://docs.python.org/3/library/dataclasses.html). Quart-Schema also generates [swagger documenation](https://swagger.io/docs/) so other developers can interact with the API with ease.
- [Quart-CORS](https://gitlab.com/pgjones/quart-cors) - Quart-CORS is an extension for the Quart microframework. It enables and controls [Cross Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).
-  [Databases](https://pypi.org/project/databases/) - The databases package provides a wrapper around the SQLAlchemy Core language and provides support for PostgreSQL, MySQL, and SQLite.
-  [Black](https://black.readthedocs.io/en/stable/) - The black formatter formats  code to the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.

### How to run the app
1. Clone or download the respository
2. Open the repository in your terminal by using ``cd``
    ```
    cd error-monitoring-api
    ```
    Create a virtual environment to manage dependencies:
    
    On Linux/MacOS:
    ```
    python3 -m venv venv
    ```
    On Windows using CMD:
    ```
    C:\>C:\Python35\python -m venv venv
    ```
3. Activate the virtual environment
    
    On Linux/MacOS:
    ```
    source venv/bin/activate
    ```
    On Windows using CMD:
    ```
    C:\> venv\Scripts\activate.bat
    ```
3. Install the dependencies within the virtual environment:
    ```
    pip install -r requirements.txt
    ```
4. Create a ``.env`` file within the root directory.
5. Define the values for the environment variables, including the secret key and the database user's username and password:
    ```
    SECRET_KEY=changethis
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
    POSTGRES_DATABASE=database
    QUART_ENV=development
    ```
6. Define the ``QUART_APP`` environment variable:
    
    On Linux/MacOS:
    ```
    export QUART_APP=app:app
    ```
    On Windows using CMD:
    ```
    set QUART_APP=app:app
    ```
7. Run the app
```
quart run
```
8. Make sure it says it connected to the database successfully. If so, it should display this:
   ```
    * Serving Quart app 'src'
    * Environment: development
    * Debug mode: True
    * Running on http://127.0.0.1:5000 (CTRL + C to quit)
    development
    [2021-09-17 16:01:48,598] INFO in __init__: Connected to database testing on port 5432
   ``` 
9.  Go to [localhost:5000](http://localhost:5000) in your browser. You should see "Hello World!" Congratulations!

### Contributions
All contributions are welcome, even small ones :) But please format your code by using this command before you make a pull request or contribution:

On Windows/MacOS/Linux:
```
black .
``` 

### API Documentation
You can view documentation for this API by visiting [localhost:5000/redocs](http://localhost:5000/redocs) or [localhost:5000/docs](http:localhost:5000/docs) 

### Roadmap
Check out the tasks on the [Projects](https://github.com/cameronthecoder/error-monitoring-api/projects/) tab