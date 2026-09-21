import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db

from fastapi.testclient import TestClient
from app.main import app

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

def test_create_product():
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