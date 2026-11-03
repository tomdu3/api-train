from flask import Flask

# Flask application instance
app = Flask(__name__)

from api_train import routes  # noqa: E402, F401


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
