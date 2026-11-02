from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200


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
    3: {
        "id": 3,
        "name": "Monitor",
        "description": "24 inch IPS monitor",
        "price": 199.99,
        "in_stock": True,
    },
    4: {
        "id": 4,
        "name": "Webcam",
        "description": "1080p webcam",
        "price": 49.99,
        "in_stock": False,
    },
    5: {
        "id": 5,
        "name": "USB Hub",
        "description": "4-port USB 3.0 hub",
        "price": 14.99,
        "in_stock": True,
    },
    6: {
        "id": 6,
        "name": "Headphones",
        "description": "Noise-cancelling headphones",
        "price": 129.99,
        "in_stock": False,
    },
    7: {
        "id": 7,
        "name": "Microphone",
        "description": "Condenser microphone",
        "price": 89.99,
        "in_stock": True,
    },
    8: {
        "id": 8,
        "name": "Laptop Stand",
        "description": "Adjustable laptop stand",
        "price": 24.99,
        "in_stock": True,
    },
    9: {
        "id": 9,
        "name": "Desk Lamp",
        "description": "LED desk lamp",
        "price": 34.99,
        "in_stock": False,
    },
    10: {
        "id": 10,
        "name": "Office Chair",
        "description": "Ergonomic office chair",
        "price": 149.99,
        "in_stock": True,
    },
    11: {
        "id": 11,
        "name": "Standing Desk",
        "description": "Adjustable standing desk",
        "price": 299.99,
        "in_stock": False,
    },
    12: {
        "id": 12,
        "name": "Monitor Arm",
        "description": "Single monitor arm",
        "price": 59.99,
        "in_stock": True,
    },
    13: {
        "id": 13,
        "name": "USB Flash Drive",
        "description": "32GB USB 3.0 flash drive",
        "price": 9.99,
        "in_stock": True,
    },
    14: {
        "id": 14,
        "name": "External Hard Drive",
        "description": "1TB external hard drive",
        "price": 79.99,
        "in_stock": False,
    },
    15: {
        "id": 15,
        "name": "Laptop Sleeve",
        "description": "15-inch laptop sleeve",
        "price": 19.99,
        "in_stock": True,
    },
}

next_product_id = 16

@app.get('/products')
def get_products():
    return jsonify(list(products.values())),200

@app.get('/products/<int:product_id>')
def get_products_by_id(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product),200
    return jsonify({'error': 'Product not found'}),404

@app.post('/products/')
def add_products():
    global next_product_id
    
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400
    
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    in_stock = data.get('in_stock', True)

    if not isinstance(name, str) or not name.strip():
        return jsonify({'error': 'Product name is required'}), 400
    
    if not isinstance(description, str):
        return jsonify({'error': 'Description must be a string'}), 400
    
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price <=0:
        return jsonify({'error': 'Price must be a positive number'}), 400

    if not isinstance(in_stock, bool):
        return jsonify({'error': 'In stock must be a boolean'}), 400
    
    product = {
        'id': next_product_id,
        'name': name.strip(),
        'description': description,
        'price': float(price),
        'in_stock': in_stock,
    }

    products[next_product_id] = product
    next_product_id += 1

    return jsonify(product), 201

def main() -> None:
    app.run(debug=True)


if __name__ == '__main__':
    main()