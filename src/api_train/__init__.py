from flask import Flask, jsonify

app = Flask(__name__)

@app.get('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200

def main() -> None:
    app.run(debug=True)

if __name__ == '__main__':
    main()
