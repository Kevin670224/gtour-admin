from flask import Blueprint, request, jsonify
from models import Product

api_product_bp = Blueprint("api_product", __name__, url_prefix="/api")

@api_product_bp.route("/products", methods=["GET"])
def get_products():
    region = request.args.get("region")

    if not region:
        return jsonify([])

    products = Product.query.filter_by(region=region).all()
    product_list = [{"id": p.id, "name": p.name} for p in products]

    return jsonify(product_list)
