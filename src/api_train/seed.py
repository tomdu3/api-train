from decimal import Decimal

from api_train import create_app, db
from api_train.models import Product
from api_train.old_db import products


def seed_database() -> None:
    app = create_app()

    with app.app_context():
        db.create_all()

        inserted_count = 0
        for item in products.values():
            product = Product(
                name=item.get("name"),
                description=item.get("description"),
                price=Decimal(str(item.get("price"))),
                in_stock=item.get("in_stock"),
            )
            db.session.add(product)
            inserted_count += 1

        db.session.commit()
        print(f"Seeded {inserted_count} products into the database.")


if __name__ == "__main__":
    seed_database()
