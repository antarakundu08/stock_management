import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app
from database import db
from models.product import Product


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory DB for testing

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_add_product(client):
    """Test creating a new product"""
    response = client.post("/product", json={
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1200.50,
        "total_quantity": 100,
        "available_quantity": 80
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Laptop"
    assert data["need_restock"] is False


def test_get_products(client):
    """Test retrieving all products"""
    client.post("/product", json={
        "name": "Phone",
        "description": "Android phone",
        "price": 500,
        "total_quantity": 50,
        "available_quantity": 10
    })
    response = client.get("/product")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Phone"


def test_get_product_by_id(client):
    """Test retrieving a single product by ID"""
    res = client.post("/product", json={
        "name": "Tablet",
        "description": "10-inch tablet",
        "price": 300,
        "total_quantity": 20,
        "available_quantity": 2
    })
    product_id = res.get_json()["id"]

    response = client.get(f"/product/{product_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Tablet"


def test_update_product(client):
    """Test updating product details"""
    res = client.post("/product", json={
        "name": "Mouse",
        "description": "Wireless mouse",
        "price": 20,
        "total_quantity": 50,
        "available_quantity": 50
    })
    product_id = res.get_json()["id"]

    response = client.put(f"/product/{product_id}", json={
        "price": 25,
        "available_quantity": 5
    })
    data = response.get_json()
    assert data["price"] == 25
    assert data["available_quantity"] == 5
    assert data["need_restock"] is True  # Since 5 < 20% of 50


def test_delete_product(client):
    """Test deleting a product"""
    res = client.post("/product", json={
        "name": "Keyboard",
        "description": "Mechanical keyboard",
        "price": 70,
        "total_quantity": 30,
        "available_quantity": 30
    })
    product_id = res.get_json()["id"]

    response = client.delete(f"/product/{product_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Product deleted"

    # Verify deletion
    response = client.get(f"/product/{product_id}")
    assert response.status_code == 404


def test_check_restock(client):
    """Test restock check logic"""
    res = client.post("/product", json={
        "name": "Charger",
        "description": "Fast charger",
        "price": 40,
        "total_quantity": 100,
        "available_quantity": 10
    })
    product_id = res.get_json()["id"]

    response = client.get(f"/restock/{product_id}")
    data = response.get_json()
    assert data["need_restock"] is True


def test_update_restock_status(client):
    """Test manually updating restock status"""
    res = client.post("/product", json={
        "name": "Monitor",
        "description": "HD monitor",
        "price": 150,
        "total_quantity": 50,
        "available_quantity": 25
    })
    product_id = res.get_json()["id"]

    response = client.put(f"/restock/update/{product_id}", json={"need_restock": True})
    data = response.get_json()
    assert data["need_restock"] is True


def test_restock_list(client):
    """Test listing all products needing restock"""
    client.post("/product", json={
        "name": "Cable",
        "description": "USB cable",
        "price": 5,
        "total_quantity": 100,
        "available_quantity": 10  # Should need restock
    })
    client.post("/product", json={
        "name": "Powerbank",
        "description": "10000mAh",
        "price": 50,
        "total_quantity": 100,
        "available_quantity": 90  # No restock needed
    })

    response = client.get("/restock/list")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Cable"
