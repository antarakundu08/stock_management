from flask import Blueprint, jsonify, request
from models.product import Product
from services.product_service import check_restock
from database import db

restock_bp = Blueprint("restock", __name__)

@restock_bp.route("/restock/<int:id>", methods=["GET"])
def check_product_restock(id):
    product = Product.query.get_or_404(id)
    product.need_restock = check_restock(product)
    db.session.commit()
    return jsonify({"id": product.id, "need_restock": product.need_restock})

@restock_bp.route("/restock/update/<int:id>", methods=["PUT"])
def update_restock_status(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.need_restock = data.get("need_restock", product.need_restock)
    db.session.commit()
    return jsonify(product.to_dict())

@restock_bp.route("/restock/list", methods=["GET"])
def restock_list():
    products = Product.query.filter_by(need_restock=True).all()
    return jsonify([p.to_dict() for p in products])
