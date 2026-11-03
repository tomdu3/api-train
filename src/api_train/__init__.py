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

    from api_train.routes import products_bp, health_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(health_bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
