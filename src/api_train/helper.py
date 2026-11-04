import re
from decimal import Decimal, InvalidOperation


def validate_name(name):
    if (
        not isinstance(name, str)
        or not name.strip()
        or not re.match(r"^[A-Za-z0-9 ]+$", name)
    ):
        return (
            None,
            "Product name is required and must contain only letters, numbers, and spaces",
        )
    return name.strip(), None


def validate_description(description):
    if not isinstance(description, str):
        return None, "Description must be a string"
    return description, None


def validate_price(price):
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return None, "Price must be a positive number"
    try:
        decimal_price = Decimal(str(price))
    except InvalidOperation:
        return None, "Price must be a positive number"
    if decimal_price <= 0:
        return None, "Price must be a positive number"
    return decimal_price, None


def validate_in_stock(in_stock):
    if not isinstance(in_stock, bool):
        return None, "In stock must be a boolean"
    return in_stock, None


def validate_product(data):
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object"

    name, error = validate_name(data.get("name"))
    if error:
        return None, error

    description, error = validate_description(data.get("description").strip())
    if error:
        return None, error

    price, error = validate_price(data.get("price"))
    if error:
        return None, error

    in_stock, error = validate_in_stock(data.get("in_stock", True))
    if error:
        return None, error

    cleaned = {
        "name": name,
        "description": description,
        "price": price,
        "in_stock": in_stock,
    }
    return cleaned, None


def invalid_properties_check(data):
    """Check if the request body contains any valid properties."""
    allowed_properties = {"name", "description", "price", "in_stock"}
    invalid_properties = []

    for prop in data:
        if prop.lower() in allowed_properties:
            continue
        else:
            invalid_properties.append(prop)

    return invalid_properties if invalid_properties else None


def validate_partial_properties(product, data):
    # validate each property
    if "name" in data:
        name, error = validate_name(data.get("name"))
        if error:
            return None, error
        product.name = name
    if "description" in data:
        description, error = validate_description(data.get("description"))
        if error:
            return None, error
        product.description = description
    if "price" in data:
        price, error = validate_price(data.get("price"))
        if error:
            return None, error
        product.price = price
    if "in_stock" in data:
        in_stock, error = validate_in_stock(data.get("in_stock"))
        if error:
            return None, error
        product.in_stock = in_stock
    return product, None
