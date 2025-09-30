from models.product import Product
from database import db

def check_restock(product: Product):
    """Auto-calculate restock status based on 20% rule."""
    if product.total_quantity == 0:
        return True
    return product.available_quantity < 0.2 * product.total_quantity

def create_product(data):
    product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        total_quantity=data["total_quantity"],
        available_quantity=data["available_quantity"]
    )
    product.need_restock = check_restock(product)
    db.session.add(product)
    db.session.commit()
    return product

def update_product(product, data):
    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.total_quantity = data.get("total_quantity", product.total_quantity)
    product.available_quantity = data.get("available_quantity", product.available_quantity)
    product.need_restock = check_restock(product)
    db.session.commit()
    return product
