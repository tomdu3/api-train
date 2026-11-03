import re
from decimal import Decimal, InvalidOperation
from flask import Blueprint, jsonify, request
from api_train import db
from api_train.models import Product
from api_train.old_db import next_product_id, products

products_bp = Blueprint("products", __name__, url_prefix="/api/v1")
health_bp = Blueprint("health", __name__, url_prefix="/api/v1")


# Health check endpoint
@health_bp.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


# Routes / CRUD Endpoints
@products_bp.get("/products")
def get_products():
    result = list(products.values())
    in_stock_filter = request.args.get("in_stock", None)
    if in_stock_filter is not None:
        in_stock_filter = in_stock_filter.lower() == "true"
        result = [
            product for product in result if product.get("in_stock") == in_stock_filter
        ]

    return jsonify(result), 200


@products_bp.get("/products/<int:product_id>")
def get_products_by_id(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404


@products_bp.post("/products/")
def add_products():
    global next_product_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    in_stock = data.get("in_stock", True)

    if (
        not isinstance(name, str)
        or not name.strip()
        or not re.match(r"^[A-Za-z0-9 ]+$", name)
    ):
        return jsonify(
            {
                "error": "Product name is required and must contain only letters and numbers and spaces"
            }
        ), 400

    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400

    if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
        return jsonify({"error": "Price must be a positive number"}), 400

    if not isinstance(in_stock, bool):
        return jsonify({"error": "In stock must be a boolean"}), 400

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


@products_bp.put("/products/<int:product_id>")
def replace_product(product_id):
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    in_stock = data.get("in_stock", True)

    if (
        not isinstance(name, str)
        or not name.strip()
        or not re.match(r"^[A-Za-z0-9 ]+$", name)
    ):
        return jsonify(
            {
                "error": "Name is required and must contain only letters and numbers and spaces"
            }
        ), 400

    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400

    if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
        return jsonify({"error": "Price must be a positive number"}), 400

    if not isinstance(in_stock, bool):
        return jsonify({"error": "In stock must be a boolean"}), 400

    product = {
        "id": product_id,
        "name": name.strip(),
        "description": description,
        "price": float(price),
        "in_stock": in_stock,
    }

    products[product_id] = product

    return jsonify(product), 200


@products_bp.patch("/products/<int:product_id>")
def update_product(product_id):
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    # check if an invalid propery is used for update
    for key in data:
        if key not in ["name", "description", "price", "in_stock"]:
            return jsonify({"error": f"Invalid property: {key}"}), 400

    product = products.get(product_id)
    name = data.get("name", None)
    description = data.get("description", None)
    price = data.get("price", None)
    in_stock = data.get("in_stock", None)

    if name is not None:
        if (
            not isinstance(name, str)
            or not name.strip()
            or not re.match(r"^[A-Za-z0-9 ]+$", name)
        ):
            return jsonify(
                {
                    "error": "Name is required and must contain only letters and numbers and spaces"
                }
            ), 400
        product["name"] = name.strip()

    if description is not None:
        if not isinstance(description, str):
            return jsonify({"error": "Description must be a string"}), 400
        product["description"] = description

    if price is not None:
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
            return jsonify({"error": "Price must be a positive number"}), 400
        product["price"] = float(price)

    if in_stock is not None:
        if not isinstance(in_stock, bool):
            return jsonify({"error": "In stock must be a boolean"}), 400
        product["in_stock"] = in_stock

    products[product_id] = product

    return jsonify(product), 200


@products_bp.delete("/products/<int:product_id>")
def delete_product(product_id):
    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404
    product = products[product_id]
    del products[product_id]
    return jsonify(
        {
            "message": f"Product - id:{product.get('id')} | name: {product.get('name')}, successfully deleted"
        }
    ), 200
