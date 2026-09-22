import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db

from fastapi.testclient import TestClient
from app.main import app

import pytest
from app.models.product import Product

load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(
    bind=test_engine
)

def get_test_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Smart Inventory API"}

def test_create_product(db):
    product_data = {
        "name": "Keyboard",
        "category": "Tech",
        "price": 15,
        "stock": 7,
        "minimum_stock": 2
    }

    response = client.post("/products", json=product_data)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Keyboard"
    assert data["category"] == "Tech"
    assert data["price"] == 15
    assert data["stock"] == 7
    assert data["minimum_stock"] == 2
    assert "id" in data

def test_get_products(db):
    product = Product(
        name="Keyboard",
        category="Tech",
        price=15,
        stock=7,
        minimum_stock=2
    )

    db.add(product)
    db.commit()

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Keyboard"
    assert data[0]["category"] == "Tech"
    assert data[0]["price"] == 15
    assert data[0]["stock"] == 7
    assert data[0]["minimum_stock"] == 2

def test_get_product_by_id(db):
    product = Product(
        name="Keyboard",
        category="Tech",
        price=15,
        stock=7,
        minimum_stock=2
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.get(f"/products/{product.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product.id
    assert data["name"] == "Keyboard"
    assert data["category"] == "Tech"
    assert data["price"] == 15
    assert data["stock"] == 7
    assert data["minimum_stock"] == 2

def test_get_product_not_found(db):
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }


def test_update_product(db):
    product = Product(
        name="Keyboard",
        category="Tech",
        price=15,
        stock=7,
        minimum_stock=2
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    update_data = {
        "price": 20,
        "stock": 10
    }

    response = client.patch(
        f"/products/{product.id}",
        json=update_data
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product.id
    assert data["name"] == "Keyboard"
    assert data["price"] == 20
    assert data["stock"] == 10
    assert data["minimum_stock"] == 2


def test_update_product_not_found(db):
    update_data = {
        "price": 20
    }

    response = client.patch(
        "/products/999",
        json=update_data
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }


def test_delete_product(db):
    product = Product(
        name="Keyboard",
        category="Tech",
        price=15,
        stock=7,
        minimum_stock=2
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.delete(
        f"/products/{product.id}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Product deleted"
    }

    deleted_product = (
        db.query(Product)
        .filter(Product.id == product.id)
        .first()
    )

    assert deleted_product is None


def test_delete_product_not_found(db):
    response = client.delete("/products/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }

@pytest.fixture
def db():
    db = TestSessionLocal()

    print("Setup")

    db.query(Product).delete()
    db.commit()

    yield db

    print ("Cleanup")
    
    db.query(Product).delete()
    db.commit()

    db.close()