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


def validate_properties_exist(data):
    """Check if the request body contains any valid properties."""
    allowed_properties = {"name", "description", "price", "in_stock"}

    for prop in data:
        if prop.lower() in allowed_properties:
            return None, None

    return None, "No valid properties provided"
