from flask import Blueprint, request, jsonify
from models.product import Product
from services.product_service import create_product, update_product
from database import db

product_bp = Blueprint("product", __name__)

@product_bp.route("/product", methods=["POST"])
def add_product():
    data = request.get_json()
    product = create_product(data)
    return jsonify(product.to_dict()), 201

@product_bp.route("/product", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@product_bp.route("/product/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@product_bp.route("/product/<int:id>", methods=["PUT"])
def update_product_route(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product = update_product(product, data)
    return jsonify(product.to_dict())

@product_bp.route("/product/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})
