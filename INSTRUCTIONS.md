# Live Coding Interview Preparation: Flask API with `uv`

A step-by-step preparation guide for building and explaining a small
Python REST API during a live coding interview.

> **Goal:** Be able to create a clean, working API from an empty folder,
> explain each decision, handle common edge cases, and test the result
> confidently.
>
> **Suggested framework:** Flask, because you have used it before and
> the interview brief mentioned Flask. The same ideas transfer to
> FastAPI or other Python frameworks.
>
> **Python environment and dependencies:** Use
> [`uv`](https://docs.astral.sh/uv/) throughout. You do not need to
> activate the virtual environment manually when you use `uv run`.

------------------------------------------------------------------------

## Contents

1.  [How to use this guide](#1-how-to-use-this-guide)
2.  [What the interviewer may be looking
    for](#2-what-the-interviewer-may-be-looking-for)
3.  [The preparation strategy](#3-the-preparation-strategy)
4.  [Install and understand `uv`](#4-install-and-understand-uv)
5.  [Create the project](#5-create-the-project)
6.  [Build the first Flask endpoint](#6-build-the-first-flask-endpoint)
7.  [Understand HTTP and REST
    basics](#7-understand-http-and-rest-basics)
8.  [Build a complete CRUD API](#8-build-a-complete-crud-api)
9.  [Validate incoming data
    properly](#9-validate-incoming-data-properly)
10. [Add a database with SQLite and
    SQLAlchemy](#10-add-a-database-with-sqlite-and-sqlalchemy)
11. [Organise the application](#11-organise-the-application)
12. [Write automated tests with
    pytest](#12-write-automated-tests-with-pytest)
13. [Useful API improvements](#13-useful-api-improvements)
14. [Connect a frontend to the API](#14-connect-a-frontend-to-the-api)
15. [Python concepts to revise](#15-python-concepts-to-revise)
16. [Live-coding approach and
    communication](#16-live-coding-approach-and-communication)
17. [Three-day preparation plan](#17-three-day-preparation-plan)
18. [Practice exercises](#18-practice-exercises)
19. [Interview-day checklist](#19-interview-day-checklist)
20. [Quick reference](#20-quick-reference)

------------------------------------------------------------------------

## 1. How to use this guide

Do not try to memorise every line of code. The important thing is to
understand the purpose of each part and be able to recreate the basic
structure without copying.

Work through the guide in this order:

1.  Get a minimal Flask application running.
2.  Create the API endpoints using in-memory data.
3.  Add validation and correct HTTP status codes.
4.  Add SQLite persistence.
5.  Add tests.
6.  Practise building a smaller API from scratch under a time limit.

For the interview, a small working solution with clear reasoning is
usually better than a large, unfinished solution with unnecessary
architecture.

### A note about scope

The exercise you were told about is to make an API with Flask, but the
exact requirements, database, and evaluation criteria are not known.
This guide therefore prepares you for common API-building tasks rather
than assuming a particular Curaleaf exercise or internal technology
stack.

Use fictional, ordinary example data. Do not use real patient
information or assume that a practice exercise requires implementing
healthcare or medical-data rules.

------------------------------------------------------------------------

## 2. What the interviewer may be looking for

A live API exercise can assess several things at once:

  -----------------------------------------------------------------------
  Area                                What to demonstrate
  ----------------------------------- -----------------------------------
  Problem solving                     Clarify the task and break it into
                                      small steps

  Python                              Use functions, dictionaries, lists,
                                      exceptions, and types sensibly

  HTTP and REST                       Choose appropriate routes, methods,
                                      and status codes

  Flask                               Understand routing, request data,
                                      responses, and app configuration

  Validation                          Reject missing, malformed, or
                                      invalid input

  Data handling                       Create, retrieve, update, and
                                      delete records correctly

  Database knowledge                  Understand basic SQL and
                                      persistence if a database is needed

  Testing                             Test success cases and common
                                      failure cases

  Communication                       Explain what you are doing and why

  Debugging                           Read errors, isolate the problem,
                                      and make a controlled fix
  -----------------------------------------------------------------------

You do not need to demonstrate every advanced technique. Start with the
smallest complete solution and add complexity only when the requirements
call for it.

### Flask or FastAPI?

For this exercise, Flask is a sensible default because it was mentioned
and you have some previous experience with it. FastAPI is also a capable
choice, but there is little benefit in switching frameworks just to use
something different.

Focus on being fluent in the framework you choose:

-   How a route is declared.
-   How request JSON is read.
-   How a response and status code are returned.
-   How invalid input is handled.
-   How the application is tested.

------------------------------------------------------------------------

## 3. The preparation strategy

Use one practice project throughout the guide: a **Product Management
API**.

A product can have:

-   `id`: unique integer identifier.
-   `name`: non-empty string.
-   `description`: optional string.
-   `price`: positive number.
-   `in_stock`: boolean.

The API will support:

  Method   Endpoint           Purpose
  -------- ------------------ --------------------------------
  GET      `/health`          Check that the API is running
  GET      `/products`        List all products
  GET      `/products/<id>`   Retrieve one product
  POST     `/products`        Create a product
  PUT      `/products/<id>`   Replace a product
  PATCH    `/products/<id>`   Update selected product fields
  DELETE   `/products/<id>`   Delete a product

This project covers the core patterns likely to appear in a simple API
exercise.

### Why start with in-memory data?

Initially, store products in a Python dictionary. This lets you
concentrate on HTTP, Flask, and validation without also debugging
database configuration.

The limitation is that the data disappears when the application stops.
Later, replace the dictionary with SQLite and SQLAlchemy.

------------------------------------------------------------------------

## 4. Install and understand `uv`

`uv` manages Python versions, project environments, dependencies, and
lockfiles. It is a convenient way to keep the project reproducible.

### 4.1 Install `uv`

On Linux, the official installer is:

``` bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a new terminal if necessary, then check:

``` bash
uv --version
```

If your shell cannot find `uv`, follow the installation instructions for
your shell and ensure the installation directory is on your `PATH`.

Official documentation: <https://docs.astral.sh/uv/>

### 4.2 Understand the important commands

  -----------------------------------------------------------------------
  Command                             What it does
  ----------------------------------- -----------------------------------
  `uv init`                           Creates a new Python project

  `uv python list`                    Lists Python versions available to
                                      `uv`

  `uv python install 3.12`            Installs Python 3.12 managed by
                                      `uv`

  `uv python pin 3.12`                Selects Python 3.12 for this
                                      project

  `uv add flask`                      Adds Flask as a project dependency

  `uv add --dev pytest ruff`          Adds pytest and Ruff as development
                                      dependencies

  `uv run python app.py`              Runs a command inside the project
                                      environment

  `uv run pytest`                     Runs the test suite in the project
                                      environment

  `uv run ruff check .`               Runs Ruff against the project

  `uv sync`                           Synchronises the environment with
                                      the project lockfile

  `uv lock`                           Updates or creates the lockfile

  `uv tree`                           Shows the dependency tree
  -----------------------------------------------------------------------

You generally do not need to run `source .venv/bin/activate`. `uv run`
automatically uses the project's environment.

### 4.3 Should you pin Python 3.12?

Python 3.12 is a reasonable choice for a practice project, but do not
change versions without a reason. Check what is already installed and
what your project declares.

For example:

``` bash
uv python install 3.12
uv python pin 3.12
```

The pin is recorded in a `.python-version` file. Your `pyproject.toml`
also declares the Python versions the project supports. Keep those
settings compatible.

------------------------------------------------------------------------

## 5. Create the project

### 5.1 Create a project folder

``` bash
mkdir flask-api-practice
cd flask-api-practice
uv init
```

Inspect what `uv init` created:

``` bash
ls -la
```

You should see a `pyproject.toml`, a `.python-version` file (depending
on the init options and uv version), a README, and usually a starter
Python file.

### 5.2 Add dependencies

Install Flask:

``` bash
uv add flask
```

Add development tools:

``` bash
uv add --dev pytest ruff
```

Later, when you are ready to use a database, add:

``` bash
uv add flask-sqlalchemy
```

`uv add` updates `pyproject.toml` and the lockfile. You should commit
both files to version control.

### 5.3 Suggested project structure

For the first few steps, a single `app.py` file is perfectly fine. As
the project grows, move towards this structure:

``` text
flask-api-practice/
├── app/
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
├── tests/
│   └── test_api.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

Do not create all these files immediately. Build the working version
first, then refactor when the separation makes the code easier to
understand.

### 5.4 Add a `.gitignore`

Create `.gitignore`:

``` gitignore
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
instance/
.env
*.py[cod]
```

Do not commit `.venv/` or secrets such as passwords and API keys. Do
commit `pyproject.toml` and `uv.lock`.

------------------------------------------------------------------------

## 6. Build the first Flask endpoint

Create `app.py`:

``` python
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)
```

Run it:

``` bash
uv run python app.py
```

Flask will print a local address, normally `http://127.0.0.1:5000`.

In another terminal, test the endpoint:

``` bash
curl http://127.0.0.1:5000/health
```

Expected response:

``` json
{
  "status": "ok"
}
```

### Understand each part

``` python
from flask import Flask, jsonify
```

Imports the Flask application class and a helper that converts Python
data into a JSON response.

``` python
app = Flask(__name__)
```

Creates the Flask application. `__name__` helps Flask identify the
location of the application and its resources.

``` python
@app.get("/health")
```

Registers a route that responds to HTTP GET requests at `/health`. Flask
also supports decorators such as `@app.post`, `@app.put`, and
`@app.delete`.

``` python
def health_check():
```

The function Flask calls when a request matches that route.

``` python
return jsonify({"status": "ok"}), 200
```

Returns JSON and the HTTP status code 200 (OK).

``` python
if __name__ == "__main__":
```

Runs the development server only when this file is executed directly. It
does not run when another module imports `app.py`.

### Development server warning

`debug=True` is useful locally because Flask can show detailed errors
and reload after code changes. Do not use Flask's development server or
debug mode as a production deployment setup.

------------------------------------------------------------------------

## 7. Understand HTTP and REST basics

An API lets another program communicate with your application using
requests and responses.

A typical request contains:

-   An HTTP method, such as GET or POST.
-   A URL, such as `/products/12`.
-   Optional headers, such as `Content-Type: application/json`.
-   Optional data in the request body.

A response contains:

-   A status code.
-   Headers.
-   Often a JSON body.

### 7.1 Common HTTP methods

  Method   Typical meaning               Example
  -------- ----------------------------- -------------------------------------
  GET      Read data                     Get all products
  POST     Create a resource             Create a product
  PUT      Replace a resource            Replace all editable product fields
  PATCH    Partially update a resource   Change only the price
  DELETE   Remove a resource             Delete a product

### 7.2 Common status codes

  -----------------------------------------------------------------------
  Code                    Meaning                 When to use it
  ----------------------- ----------------------- -----------------------
  200                     OK                      Successful read or
                                                  update with a response
                                                  body

  201                     Created                 A resource was
                                                  successfully created

  204                     No Content              Successful operation
                                                  with no response body

  400                     Bad Request             The request is
                                                  malformed or fails
                                                  validation

  404                     Not Found               The requested resource
                                                  does not exist

  405                     Method Not Allowed      The route exists, but
                                                  not for that HTTP
                                                  method

  409                     Conflict                The request conflicts
                                                  with current resource
                                                  state

  500                     Internal Server Error   An unexpected
                                                  server-side failure
  -----------------------------------------------------------------------

Choose status codes consistently. For example, do not return 200 when a
new resource has been created if 201 is more appropriate.

### 7.3 What is REST?

REST is an architectural style for designing networked APIs. In a simple
resource-oriented API:

-   URLs identify resources, usually using nouns (`/products`).
-   HTTP methods describe the operation.
-   Responses use meaningful status codes.
-   Requests should be understandable independently.

Prefer:

``` text
GET    /products
GET    /products/5
POST   /products
DELETE /products/5
```

Over action-heavy URLs such as:

``` text
/getAllProducts
/createNewProduct
/deleteProduct/5
```

------------------------------------------------------------------------

## 8. Build a complete CRUD API

CRUD stands for Create, Read, Update, and Delete.

For now, use a dictionary as a temporary data store. Replace the starter
content of `app.py` with the following complete version.

``` python
from flask import Flask, jsonify, request

app = Flask(__name__)

products = {
    1: {
        "id": 1,
        "name": "Keyboard",
        "description": "Mechanical keyboard",
        "price": 79.99,
        "in_stock": True,
    },
    2: {
        "id": 2,
        "name": "Mouse",
        "description": "Wireless mouse",
        "price": 29.99,
        "in_stock": True,
    },
}

next_product_id = 3


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.get("/products")
def get_products():
    return jsonify(list(products.values())), 200


@app.get("/products/<int:product_id>")
def get_product(product_id):
    product = products.get(product_id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


@app.post("/products")
def create_product():
    global next_product_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    name = data.get("name")
    description = data.get("description", "")
    price = data.get("price")
    in_stock = data.get("in_stock", True)

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400

    # bool is a subclass of int in Python, so reject booleans explicitly.
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
        return jsonify({"error": "Price must be a positive number"}), 400

    if not isinstance(in_stock, bool):
        return jsonify({"error": "in_stock must be a boolean"}), 400

    product = {
        "id": next_product_id,
        "name": name.strip(),
        "description": description,
        "price": float(price),
        "in_stock": in_stock,
    }

    products[next_product_id] = product
    next_product_id += 1

    return jsonify(product), 201


@app.put("/products/<int:product_id>")
def replace_product(product_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    name = data.get("name")
    description = data.get("description", "")
    price = data.get("price")
    in_stock = data.get("in_stock", True)

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400

    if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
        return jsonify({"error": "Price must be a positive number"}), 400

    if not isinstance(in_stock, bool):
        return jsonify({"error": "in_stock must be a boolean"}), 400

    product = {
        "id": product_id,
        "name": name.strip(),
        "description": description,
        "price": float(price),
        "in_stock": in_stock,
    }

    products[product_id] = product
    return jsonify(product), 200


@app.patch("/products/<int:product_id>")
def update_product(product_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    product = products.get(product_id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    allowed_fields = {"name", "description", "price", "in_stock"}
    unknown_fields = set(data) - allowed_fields

    if unknown_fields:
        return jsonify({
            "error": "Unknown fields",
            "fields": sorted(unknown_fields),
        }), 400

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "Name must be a non-empty string"}), 400
        product["name"] = name.strip()

    if "description" in data:
        if not isinstance(data["description"], str):
            return jsonify({"error": "Description must be a string"}), 400
        product["description"] = data["description"]

    if "price" in data:
        price = data["price"]
        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or price <= 0
        ):
            return jsonify({"error": "Price must be a positive number"}), 400
        product["price"] = float(price)

    if "in_stock" in data:
        if not isinstance(data["in_stock"], bool):
            return jsonify({"error": "in_stock must be a boolean"}), 400
        product["in_stock"] = data["in_stock"]

    return jsonify(product), 200


@app.delete("/products/<int:product_id>")
def delete_product(product_id):
    product = products.pop(product_id, None)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
```

Run it:

``` bash
uv run python app.py
```

### 8.1 Test each endpoint with curl

Open a second terminal while the Flask server is running.

List products:

``` bash
curl -i http://127.0.0.1:5000/products
```

Get product 1:

``` bash
curl -i http://127.0.0.1:5000/products/1
```

Try a product that does not exist:

``` bash
curl -i http://127.0.0.1:5000/products/999
```

Create a product:

``` bash
curl -i -X POST http://127.0.0.1:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monitor",
    "description": "27-inch monitor",
    "price": 199.99,
    "in_stock": true
  }'
```

Replace a product:

``` bash
curl -i -X PUT http://127.0.0.1:5000/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Keyboard Pro",
    "description": "Updated mechanical keyboard",
    "price": 99.99,
    "in_stock": true
  }'
```

Partially update a product:

``` bash
curl -i -X PATCH http://127.0.0.1:5000/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 89.99}'
```

Delete a product:

``` bash
curl -i -X DELETE http://127.0.0.1:5000/products/1
```

### 8.2 Understand the implementation

**The dictionary**

``` python
products = {1: {...}, 2: {...}}
```

The key is the product ID. This makes looking up a product by ID
straightforward.

**The URL converter**

``` python
@app.get("/products/<int:product_id>")
```

Flask converts the URL segment to an integer before passing it to the
function.

**Reading JSON**

``` python
data = request.get_json(silent=True)
```

This attempts to parse the request body as JSON. With `silent=True`,
invalid or missing JSON produces `None` instead of raising a parsing
error. The route then checks the result and returns a controlled 400
response.

**Returning JSON**

``` python
return jsonify(product), 200
```

`jsonify` serialises the Python dictionary into a JSON response.

**Creating a resource**

``` python
return jsonify(product), 201
```

201 communicates that the resource was created.

**Deleting a resource**

``` python
return "", 204
```

204 means the request succeeded and there is no response body. Do not
return a JSON body with a 204 response.

### 8.3 Important limitation of the in-memory version

This implementation is designed for learning. It has several
limitations:

-   All data is lost when the process restarts.
-   It is not safe for concurrent writes in a real multi-worker
    application.
-   The global `next_product_id` is only a simple practice solution.
-   Validation is repeated between routes.
-   A real application should use a database and a more robust
    validation layer.

These are good points to explain if asked how you would improve the
solution.

------------------------------------------------------------------------

## 9. Validate incoming data properly

Never assume that a client sends valid data. Clients can make mistakes,
and requests can be malformed or deliberately unexpected.

For the product API, consider these cases:

  Field           Valid example   Invalid example
  --------------- --------------- ------------------------------
  `name`          `"Keyboard"`    `""`, `null`, `42`
  `description`   `"Wireless"`    `42`, `null`
  `price`         `19.99`         `0`, `-5`, `"cheap"`, `true`
  `in_stock`      `true`          `"yes"`, `1`, `null`

### 9.1 Why check booleans separately?

In Python:

``` python
isinstance(True, int)  # True
```

This is because `bool` is a subclass of `int`. If a field must be a
number, but not a boolean, check `isinstance(value, bool)` first.

### 9.2 Why use `.strip()`?

``` python
name.strip()
```

Removes whitespace from the start and end of a string. This means
`"   "` is rejected as an empty name.

### 9.3 Validate unknown fields

For PATCH requests, decide what to do if the client sends an unexpected
property:

``` json
{
  "name": "Keyboard",
  "admin": true
}
```

The practice API rejects unknown fields. This makes the API's accepted
input explicit and prevents silently accepting values that the
application does not use.

### 9.4 PUT versus PATCH

A useful distinction:

-   **PUT:** The client sends the complete editable representation and
    replaces the existing values.
-   **PATCH:** The client sends only the fields it wants to change.

For example, if the current product has a name, description, price, and
stock status, a PATCH request containing only `{"price": 25}` should
leave the other fields unchanged.

### 9.5 Money and floating-point numbers

The example uses floats to keep the exercise simple. In production
systems, floating-point arithmetic can introduce rounding surprises. For
money, consider storing integer minor units (such as pence) or using
Python's `Decimal`, with a clearly defined serialisation strategy.

------------------------------------------------------------------------

## 10. Add a database with SQLite and SQLAlchemy

Once the in-memory API works, add persistence. SQLite is a good practice
database because it does not require a separate database server.

### 10.1 Install Flask-SQLAlchemy

``` bash
uv add flask-sqlalchemy
```

### 10.2 What are SQLAlchemy and Flask-SQLAlchemy?

-   **SQL:** The language commonly used to query relational databases.
-   **SQLite:** A lightweight relational database stored in a file.
-   **SQLAlchemy:** A Python SQL toolkit and Object Relational Mapper
    (ORM).
-   **Flask-SQLAlchemy:** Flask integration that manages configuration
    and database access in a Flask application.

An ORM lets you work with Python model objects instead of writing every
SQL statement manually.

### 10.3 Create an application factory

Replace the single-file design with this structure:

``` text
app/
├── __init__.py
├── models.py
└── routes.py
```

The application factory creates and configures the Flask app. It is
especially useful for tests because tests can create an app with a
separate configuration.

Create `app/__init__.py`:

``` python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    from app.routes import products_bp
    app.register_blueprint(products_bp)

    with app.app_context():
        db.create_all()

    return app
```

Important details:

-   `db = SQLAlchemy()` creates the extension object without binding it
    to one app immediately.
-   `db.init_app(app)` connects the extension to the created app.
-   `test_config` lets tests override settings, for example to use an
    in-memory SQLite database.
-   A Blueprint groups related routes.
-   `app.app_context()` provides the application context needed by Flask
    extensions.

For a small interview exercise, `db.create_all()` can be acceptable to
get started. For a real application, use migrations (commonly
Flask-Migrate/Alembic) to manage schema changes instead of relying on
`create_all()`.

### 10.4 Define a model

Create `app/models.py`:

``` python
from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    in_stock = db.Column(db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "in_stock": self.in_stock,
        }
```

A model describes the shape of a database table.

-   `primary_key=True` makes `id` the primary key.
-   `nullable=False` means the column must have a value.
-   `String(120)` sets a maximum string length at the database-model
    level.
-   `Numeric(10, 2)` is appropriate for fixed-precision decimal values
    such as prices.
-   `to_dict()` gives the API a predictable JSON-friendly
    representation. Here the Decimal-like price is represented as a
    string to avoid silently converting it to an imprecise float.

### 10.5 Add database routes

Create `app/routes.py`:

``` python
from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request

from app import db
from app.models import Product

products_bp = Blueprint("products", __name__)


def parse_product_data(data, partial=False):
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object"

    allowed_fields = {"name", "description", "price", "in_stock"}
    unknown_fields = set(data) - allowed_fields

    if unknown_fields:
        return None, f"Unknown fields: {', '.join(sorted(unknown_fields))}"

    if not partial:
        required_fields = {"name", "price"}
        missing = required_fields - set(data)
        if missing:
            return None, f"Missing required fields: {', '.join(sorted(missing))}"

    cleaned = {}

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            return None, "Name must be a non-empty string"
        cleaned["name"] = name.strip()

    if "description" in data:
        description = data["description"]
        if not isinstance(description, str):
            return None, "Description must be a string"
        cleaned["description"] = description

    if "price" in data:
        raw_price = data["price"]

        if isinstance(raw_price, bool):
            return None, "Price must be a positive number"

        try:
            price = Decimal(str(raw_price))
        except (InvalidOperation, ValueError):
            return None, "Price must be a valid number"

        if not price.is_finite() or price <= 0:
            return None, "Price must be a positive number"

        cleaned["price"] = price.quantize(Decimal("0.01"))

    if "in_stock" in data:
        in_stock = data["in_stock"]
        if not isinstance(in_stock, bool):
            return None, "in_stock must be a boolean"
        cleaned["in_stock"] = in_stock

    return cleaned, None


@products_bp.get("/products")
def get_products():
    products = db.session.execute(
        db.select(Product).order_by(Product.id)
    ).scalars().all()

    return jsonify([product.to_dict() for product in products]), 200


@products_bp.get("/products/<int:product_id>")
def get_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product.to_dict()), 200


@products_bp.post("/products")
def create_product():
    data = request.get_json(silent=True)
    cleaned, error = parse_product_data(data)

    if error:
        return jsonify({"error": error}), 400

    product = Product(**cleaned)
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@products_bp.patch("/products/<int:product_id>")
def update_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json(silent=True)
    cleaned, error = parse_product_data(data, partial=True)

    if error:
        return jsonify({"error": error}), 400

    for field, value in cleaned.items():
        setattr(product, field, value)

    db.session.commit()
    return jsonify(product.to_dict()), 200


@products_bp.delete("/products/<int:product_id>")
def delete_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return "", 204
```

This example includes GET, POST, PATCH, and DELETE to demonstrate the
database pattern. Add PUT if the task requires it, using full-field
validation rather than partial validation.

### 10.6 Add an entry point

Create `run.py`:

``` python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

Run:

``` bash
uv run python run.py
```

### 10.7 Understand the database operations

  Code                                       Meaning
  ------------------------------------------ ------------------------------------
  `db.session.add(product)`                  Mark a new object for insertion
  `db.session.commit()`                      Commit the transaction
  `db.session.get(Product, product_id)`      Find a row by primary key
  `db.session.execute(db.select(Product))`   Execute a SELECT query
  `.scalars().all()`                         Return the resulting model objects
  `db.session.delete(product)`               Mark an object for deletion

A database transaction groups operations so they can be committed
together. If an operation fails, you may need to call
`db.session.rollback()` before using that session again.

For production code, handle database exceptions carefully, roll back
failed transactions, and avoid exposing internal exception details to
clients.

------------------------------------------------------------------------

## 11. Organise the application

A common way to organise a Flask project is:

-   **Application factory:** Creates and configures the app.
-   **Blueprints:** Group related routes.
-   **Models:** Represent database entities.
-   **Validation functions or schemas:** Check incoming data.
-   **Tests:** Verify behaviour.

Do not split code into many files just for the sake of it. A useful rule
is: separate code when doing so makes responsibilities clearer or makes
testing easier.

### 11.1 What is a Blueprint?

A Blueprint is a way to group routes and register them with a Flask
application.

``` python
products_bp = Blueprint("products", __name__)

@products_bp.get("/products")
def get_products():
    ...
```

Then register it:

``` python
app.register_blueprint(products_bp)
```

This keeps product routes together and makes it easier to add other
route groups later.

### 11.2 What is an application factory?

Instead of creating one global app object, a function creates the app:

``` python
def create_app(test_config=None):
    app = Flask(__name__)
    ...
    return app
```

Benefits:

-   Tests can create a separate app with test settings.
-   Configuration is centralised.
-   Extensions can be initialised consistently.
-   The application is easier to grow.

For a timed exercise, explain why you are choosing a simple or
structured approach. If the task is tiny, one file may be the most
efficient choice.

------------------------------------------------------------------------

## 12. Write automated tests with pytest

Tests help prove that the API behaves as expected and protect against
accidental regressions.

### 12.1 Why test the API?

At minimum, test:

-   A successful request.
-   A missing resource.
-   Invalid input.
-   Creation and retrieval.
-   Update behaviour.
-   Deletion behaviour.

A test should check both the status code and important response data.

### 12.2 Configure a test app

Create `tests/test_api.py` for the application-factory version:

``` python
import pytest

from app import create_app, db
from app.models import Product


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_list_products_is_empty(client):
    response = client.get("/products")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "price": 79.99,
            "in_stock": True,
        },
    )

    assert response.status_code == 201

    body = response.get_json()
    assert body["name"] == "Keyboard"
    assert body["in_stock"] is True
    assert "id" in body


def test_create_product_rejects_missing_name(client):
    response = client.post(
        "/products",
        json={"price": 79.99},
    )

    assert response.status_code == 400


def test_get_missing_product_returns_404(client):
    response = client.get("/products/999")

    assert response.status_code == 404


def test_patch_product(client):
    create_response = client.post(
        "/products",
        json={"name": "Keyboard", "price": 79.99},
    )
    product_id = create_response.get_json()["id"]

    response = client.patch(
        f"/products/{product_id}",
        json={"price": 89.99},
    )

    assert response.status_code == 200
    assert response.get_json()["price"] == "89.99"


def test_delete_product(client):
    create_response = client.post(
        "/products",
        json={"name": "Keyboard", "price": 79.99},
    )
    product_id = create_response.get_json()["id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 204
    assert response.data == b""

    missing_response = client.get(f"/products/{product_id}")
    assert missing_response.status_code == 404
```

The tests assume you have the database-backed routes and the `health`
route registered. If you have not implemented the health route in
`routes.py`, add it or adjust the test.

Run tests:

``` bash
uv run pytest -v
```

### 12.3 Understand the test fixtures

A pytest fixture prepares something that tests can reuse.

-   The `app` fixture creates an application configured for testing.
-   The SQLite URI `sqlite://` creates an in-memory database for the
    test app.
-   The `yield` separates setup from teardown.
-   The `client` fixture gives tests Flask's test client, which makes
    requests without starting a real network server.

The app configuration is passed into `create_app` before the database
extension is initialised. This is important: changing the database URI
after the extension has already been configured may not have the effect
you expect.

### 12.4 What should you test first?

If time is limited, prioritise:

1.  `GET /products` returns 200.
2.  `POST /products` creates a product and returns 201.
3.  Invalid POST returns 400.
4.  `GET /products/<id>` returns 404 for an unknown ID.
5.  PATCH changes only the requested field.
6.  DELETE removes the record and returns 204.

------------------------------------------------------------------------

## 13. Useful API improvements

These are good follow-up improvements if the core requirements are
complete.

### 13.1 Pagination

If there are many products, returning all of them may be inefficient.

A simple API could accept:

``` text
GET /products?page=1&per_page=10
```

With Flask-SQLAlchemy, a query can be paginated:

``` python
page = request.args.get("page", 1, type=int)
per_page = request.args.get("per_page", 10, type=int)

if page < 1 or per_page < 1 or per_page > 100:
    return jsonify({"error": "Invalid pagination parameters"}), 400

pagination = db.paginate(
    db.select(Product).order_by(Product.id),
    page=page,
    per_page=per_page,
    error_out=False,
)

return jsonify({
    "items": [product.to_dict() for product in pagination.items],
    "page": pagination.page,
    "per_page": pagination.per_page,
    "total": pagination.total,
    "pages": pagination.pages,
}), 200
```

Explain that a maximum page size helps prevent a client from requesting
an unnecessarily large result set.

### 13.2 Filtering

For example:

``` text
GET /products?in_stock=true
```

Read query parameters with `request.args`. Validate them rather than
treating arbitrary strings as booleans.

### 13.3 Sorting

For example:

``` text
GET /products?sort=name
```

Only allow known sort fields. Do not use arbitrary client input to
construct raw SQL.

### 13.4 Consistent error responses

Use a predictable shape:

``` json
{
  "error": "Product not found"
}
```

For more complex validation, you could return field-specific errors:

``` json
{
  "error": "Validation failed",
  "details": {
    "name": "Name is required",
    "price": "Price must be positive"
  }
}
```

Consistency makes frontend integration easier.

### 13.5 Database migrations

When a database schema changes, migrations record and apply those
changes. In a real application, consider Flask-Migrate (built on
Alembic) rather than relying on `db.create_all()`.

### 13.6 Logging and configuration

Avoid hardcoding secrets or environment-specific settings. Use
environment variables for configuration that differs between
development, testing, and production.

Do not return stack traces or database connection details to API
clients.

------------------------------------------------------------------------

## 14. Connect a frontend to the API

You have some JavaScript and frontend experience, so be ready to explain
how a frontend might call your API. Do not spend most of your
preparation time on React unless the interview explicitly includes
frontend work.

A simple JavaScript request:

``` javascript
async function loadProducts() {
  const response = await fetch("http://127.0.0.1:5000/products");

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}
```

Example usage:

``` javascript
loadProducts()
  .then((products) => {
    console.log(products);
  })
  .catch((error) => {
    console.error(error);
  });
```

The same request using `async`/`await`:

``` javascript
async function showProducts() {
  try {
    const products = await loadProducts();
    console.log(products);
  } catch (error) {
    console.error(error);
  }
}
```

### 14.1 CORS

If the frontend and API are served from different origins, the browser
may enforce Cross-Origin Resource Sharing (CORS) rules.

For local development, Flask-CORS can help:

``` bash
uv add flask-cors
```

Then configure it deliberately:

``` python
from flask_cors import CORS

CORS(app, origins=["http://localhost:5173"])
```

Do not use unrestricted CORS in production without understanding the
security implications. Allow only the origins that should be able to
access the API.

### 14.2 What should the frontend handle?

A frontend should usually account for:

-   Loading state.
-   Successful response.
-   Empty result.
-   Validation or server error.
-   Network failure.

The API should return clear status codes and predictable response bodies
so the frontend can respond appropriately.

------------------------------------------------------------------------

## 15. Python concepts to revise

These are common Python concepts worth practising before a live coding
exercise.

### 15.1 Dictionaries

``` python
product = {
    "id": 1,
    "name": "Keyboard",
    "price": 79.99,
}

name = product["name"]
price = product.get("price")
```

-   `product["name"]` raises `KeyError` if the key is missing.
-   `product.get("name")` returns `None` by default if the key is
    missing.

### 15.2 Lists and comprehensions

``` python
products = [
    {"name": "Keyboard", "price": 79.99},
    {"name": "Mouse", "price": 29.99},
]

names = [product["name"] for product in products]
```

### 15.3 Functions and return values

``` python
def calculate_total(price, quantity):
    return price * quantity
```

Keep functions focused. A validation helper should validate; a route
should coordinate the request and response.

### 15.4 Exceptions

``` python
try:
    quantity = int("5")
except ValueError:
    print("Quantity must be an integer")
```

Use exceptions for exceptional conditions and handle expected invalid
user input deliberately.

### 15.5 Type hints

``` python
def get_product_name(product: dict) -> str:
    return product["name"]
```

Type hints make intentions clearer and can help tools catch mistakes.
They do not automatically validate incoming JSON at runtime.

### 15.6 `None` and truthiness

``` python
value = None

if value is None:
    print("No value")
```

Prefer `is None` when checking specifically for `None`. Do not confuse a
missing value with valid values such as `0`, `False`, or an empty
string.

### 15.7 `*args` and `**kwargs`

-   `*args` collects extra positional arguments.
-   `**kwargs` collects extra keyword arguments.

For example:

``` python
def create_record(**fields):
    print(fields)

create_record(name="Keyboard", price=79.99)
```

In the SQLAlchemy example, `Product(**cleaned)` passes the dictionary
entries as keyword arguments to the model constructor.

### 15.8 Mutable data

Dictionaries and lists can be changed in place:

``` python
product["price"] = 89.99
```

Be aware that assigning a variable to an existing dictionary does not
make a copy:

``` python
first = {"name": "Keyboard"}
second = first
second["name"] = "Mouse"

# first["name"] is now also "Mouse"
```

This matters when writing tests and updating nested data.

------------------------------------------------------------------------

## 16. Live-coding approach and communication

The interviewer is assessing how you work, not just whether you can type
quickly.

### 16.1 Start by clarifying the task

Before coding, ask questions such as:

-   What resources should the API manage?
-   Which operations are required?
-   Is a database required, or is in-memory storage acceptable?
-   What fields are required, and what validation rules apply?
-   Should the API support pagination or filtering?
-   Are tests expected?
-   Is there an existing project structure or should I create one?

Do not ask every question mechanically. Ask the questions that affect
your implementation.

### 16.2 Repeat your understanding

For example:

> "I'll create a REST API for products. I'll start with listing and
> retrieving products, then add creation, validation, updates, and
> deletion. I'll keep the implementation simple and add persistence if
> the requirements call for it."

This gives the interviewer a chance to correct your interpretation.

### 16.3 Work in small increments

A useful order is:

1.  Inspect the project and understand what already exists.
2.  Create or confirm the environment.
3.  Make the Flask app start.
4.  Add one endpoint.
5.  Test it.
6.  Add the remaining required endpoints.
7.  Add validation and error handling.
8.  Add tests if time allows.
9.  Review the solution and explain trade-offs.

Avoid writing a large amount of code before running it for the first
time.

### 16.4 Narrate your reasoning

You do not need to talk constantly. Explain important decisions:

-   "I'm using a dictionary first because persistence is not part of the
    requirement yet."
-   "I'm returning 404 because the requested product does not exist."
-   "I'm validating the request body before creating the database
    object."
-   "I'm separating this validation into a helper because both POST and
    PATCH need it."
-   "I would add pagination if this endpoint needed to handle a large
    collection."

### 16.5 When you get stuck

Use this sequence:

1.  Read the full error message.
2.  Identify the file and line where the failure occurs.
3.  Check the input and the value's type.
4.  Reduce the problem to a small example.
5.  Make one change at a time.
6.  Re-run the smallest relevant test.

If you do not know something, say so clearly and explain how you would
investigate it. Do not pretend to know an API or library behaviour you
are unsure about.

### 16.6 Avoid overengineering

Do not start by adding:

-   Authentication and authorisation.
-   Docker and deployment configuration.
-   A complex repository/service architecture.
-   A large validation framework.
-   Caching or background jobs.
-   Multiple database abstractions.

Add these only if the task needs them or the interviewer asks how you
would extend the solution.

------------------------------------------------------------------------

## 17. Three-day preparation plan

Adjust the hours to your energy and schedule. The goal is deliberate
practice, not staying up all night.

### Day 1 --- Flask and HTTP fundamentals

**Target: build the in-memory CRUD API without copying.**

1.  Set up the project with `uv`.
2.  Create the `/health` endpoint.
3.  Explain the Flask app and route decorator.
4.  Implement `GET /products`.
5.  Implement `GET /products/<id>`.
6.  Implement `POST /products`.
7.  Add input validation.
8.  Implement PUT, PATCH, and DELETE.
9.  Test the endpoints with curl.
10. Close the guide and recreate the core API from memory.

At the end of Day 1, you should be able to explain:

-   What a route is.
-   How Flask reads JSON.
-   How to return JSON and status codes.
-   The difference between PUT and PATCH.
-   Why validation matters.

### Day 2 --- Database and testing

**Target: understand persistence and prove the API works.**

1.  Add Flask-SQLAlchemy using `uv add flask-sqlalchemy`.
2.  Create the application factory.
3.  Define the Product model.
4.  Create the database-backed GET and POST endpoints.
5.  Add PATCH and DELETE.
6.  Run the API and test it with curl.
7.  Add pytest and create a test client.
8.  Write tests for success and failure cases.
9.  Run `uv run pytest -v`.
10. Fix any failing tests and explain why they failed.

At the end of Day 2, you should be able to explain:

-   What an ORM does.
-   What a model represents.
-   What a database transaction is.
-   What `commit()` does.
-   Why tests should use a separate test database.

### Day 3 --- Timed practice and interview rehearsal

**Target: build a small API from a blank project under time pressure.**

1.  Set a timer for 75--90 minutes.
2.  Start with a blank folder or a minimal starter project.
3.  Build the required routes for a new resource.
4.  Add validation and sensible status codes.
5.  Test the main success and failure cases.
6.  Spend 10 minutes reviewing your code.
7.  Explain your implementation aloud as if the interviewer were
    present.
8.  Repeat the exercise with a different resource if you have time.

Do not spend the final evening adding new technologies. Focus on
fluency, sleep, and being able to explain your choices.

------------------------------------------------------------------------

## 18. Practice exercises

Try these without looking at the solutions first.

### Exercise 1 --- Books API

Create a Books API with:

-   `id`
-   `title`
-   `author`
-   `published_year`

Required routes:

-   `GET /books`
-   `GET /books/<id>`
-   `POST /books`
-   `DELETE /books/<id>`

Validation:

-   Title must be a non-empty string.
-   Author must be a non-empty string.
-   Published year must be a reasonable positive integer.

### Exercise 2 --- Tasks API

Create a task resource with:

-   `id`
-   `title`
-   `completed`
-   `created_at`

Add:

-   `GET /tasks?completed=true`
-   `PATCH /tasks/<id>` to mark a task complete.
-   Validation that `completed` must be a boolean.

### Exercise 3 --- Appointment API

Create a simple appointment API with fictional data:

-   `id`
-   `title`
-   `date`
-   `duration_minutes`

Add:

-   `GET /appointments`
-   `POST /appointments`
-   `GET /appointments/<id>`
-   `DELETE /appointments/<id>`

Validation:

-   Title is required.
-   Date must use a consistent format.
-   Duration must be a positive integer.

Keep this exercise focused on ordinary scheduling data. Do not introduce
real patient information or medical rules.

### Exercise 4 --- Add pagination

Add `page` and `per_page` query parameters to one list endpoint.

Check:

-   Defaults are sensible.
-   Page and page size are positive integers.
-   Page size has a maximum.
-   The response includes items and pagination metadata.

### Exercise 5 --- Explain your design

Without looking at the guide, explain:

1.  Why did you choose Flask?
2.  What is the difference between GET and POST?
3.  What is the difference between PUT and PATCH?
4.  When should an API return 400 versus 404?
5.  What is an ORM?
6.  Why use an application factory?
7.  How would you test a route?
8.  What would you improve if the API needed to support many users?

------------------------------------------------------------------------

## 19. Interview-day checklist

### Before the interview

-   [ ] Check that `uv --version` works.
-   [ ] Check that Python is available through `uv`.
-   [ ] Make sure you can create a project and add Flask.
-   [ ] Make sure you can run a Flask app.
-   [ ] Make sure curl works.
-   [ ] Make sure you can run pytest.
-   [ ] Have a working editor and terminal setup.
-   [ ] Close unrelated applications and notifications.
-   [ ] Keep the exercise requirements visible.
-   [ ] Have water nearby.

### During the exercise

-   [ ] Clarify requirements before committing to an approach.
-   [ ] Confirm whether a database is required.
-   [ ] Start with a minimal working endpoint.
-   [ ] Build in small steps.
-   [ ] Run the code early.
-   [ ] Use appropriate status codes.
-   [ ] Validate client input.
-   [ ] Test a missing resource and invalid input.
-   [ ] Explain important decisions.
-   [ ] Leave time to review the result.

### Final review

-   [ ] Does the application start?
-   [ ] Do the required routes work?
-   [ ] Are success responses correct?
-   [ ] Are error responses understandable?
-   [ ] Are missing resources handled?
-   [ ] Is input validated?
-   [ ] Are there obvious debug prints or temporary code?
-   [ ] Can you explain the main parts of the solution?

------------------------------------------------------------------------

## 20. Quick reference

### Start a new project

``` bash
mkdir flask-api-practice
cd flask-api-practice
uv init
uv add flask
uv add --dev pytest ruff
```

### Add database dependencies

``` bash
uv add flask-sqlalchemy
```

### Run the application

``` bash
uv run python app.py
```

Or, if using the application-factory structure:

``` bash
uv run python run.py
```

### Run tests and lint

``` bash
uv run pytest -v
uv run ruff check .
```

### Run a basic endpoint test

``` bash
curl -i http://127.0.0.1:5000/health
```

### Create a product

``` bash
curl -i -X POST http://127.0.0.1:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Keyboard","price":79.99}'
```

### Remember these concepts

-   `request.get_json()` reads a JSON request body.
-   `jsonify()` creates a JSON response.
-   `request.args` reads URL query parameters.
-   `request.args.get("page", 1, type=int)` reads and converts a query
    parameter.
-   `@app.get(...)` registers a GET route.
-   `@app.post(...)` registers a POST route.
-   `db.session.add(...)` stages a database insert.
-   `db.session.commit()` commits a transaction.
-   `db.session.get(Model, id)` retrieves a record by primary key.
-   `uv add ...` adds a dependency.
-   `uv run ...` runs a command in the project environment.
-   `uv sync` synchronises the environment with the lockfile.

------------------------------------------------------------------------

## Final advice

Your strongest preparation is to build the same small API several times,
gradually reducing how much you rely on this guide.

Aim to be comfortable with the following sequence:

1.  Create a project with `uv`.
2.  Start a Flask app.
3.  Define routes.
4.  Read and validate JSON.
5.  Return the right status codes.
6.  Implement CRUD operations.
7.  Test the important cases.
8.  Explain what you would change for a production application.

You do not need to know every Flask feature. You need to show that you
can understand a requirement, make sensible choices, build a working
solution, test it, and communicate clearly while doing so.
