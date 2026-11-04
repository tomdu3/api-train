import re
from decimal import Decimal, InvalidOperation
from flask import Blueprint, jsonify, request
from api_train import db
from api_train.models import Product
from api_train.helper import (
    validate_name,
    validate_description,
    validate_price,
    validate_in_stock,
    validate_product,
    invalid_properties_check,
    validate_partial_properties,
)
# from api_train.old_db import next_product_id, products

products_bp = Blueprint("products", __name__, url_prefix="/api/v1")
health_bp = Blueprint("health", __name__, url_prefix="/api/v1")


# Health check endpoint
@health_bp.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


# Routes / CRUD Endpoints
@products_bp.get("/products")
def get_products():
    query = db.select(Product)
    in_stock_filter = request.args.get("in_stock", None)

    if in_stock_filter is not None:
        if in_stock_filter.lower() not in ["true", "false"]:
            return jsonify(
                {"error": "`in_stock` value must be boolean true or false"}
            ), 400
        in_stock_bool = in_stock_filter.lower() == "true"
        query = query.where(Product.in_stock == in_stock_bool)

    result = db.session.execute(query).scalars().all()
    return jsonify([product.to_dict() for product in result]), 200


@products_bp.get("/products/<int:product_id>")
def get_products_by_id(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200


@products_bp.post("/products/")
def add_products():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    cleaned, error = validate_product(data)
    if error:
        return jsonify({"error": error}), 400

    product = Product(**cleaned)
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@products_bp.put("/products/<int:product_id>")
def replace_product(product_id):
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    cleaned, error = validate_product(data)
    if error:
        return jsonify({"error": error}), 400

    product.name = cleaned["name"]
    product.description = cleaned["description"]
    product.price = cleaned["price"]
    product.in_stock = cleaned["in_stock"]

    db.session.commit()

    return jsonify(product.to_dict()), 200


@products_bp.patch("/products/<int:product_id>")
def update_product(product_id):
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    # check if an invalid propery is used for update
    invalid_properties = invalid_properties_check(data)
    if invalid_properties:
        return jsonify(
            {"error": f"Invalid properties: {', '.join(invalid_properties)}"}
        ), 400
    # update the product properties if the property is valid and not empty
    for key, value in data.items():
        if value is None:
            return jsonify({"error": f"Value for {key} cannot be empty"}), 400

    product, error = validate_partial_properties(product, data)
    if error:
        return jsonify({"error": error}), 400

    db.session.commit()

    return jsonify(product.to_dict()), 200


@products_bp.delete("/products/<int:product_id>")
def delete_product(product_id):
    query = db.session.execute(db.select(Product).where(Product.id == product_id))
    product = query.scalar()
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(
        {
            "message": f"Product - id:{product_id} | name: {product.name}, successfully deleted"
        }
    ), 200
